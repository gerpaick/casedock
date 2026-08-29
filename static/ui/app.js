(() => {
  document.documentElement.classList.add("js");

  const modalState = new WeakMap();
  const initializedModals = new WeakSet();
  const initializedMessages = new WeakSet();
  const messageDismissTimers = new WeakMap();
  let pendingInboxFocusReturn = null;
  const TOOLTIP_SELECTOR = "[data-history-tooltip][data-tippy-content]";
  const MESSAGE_SELECTOR = "[data-message]";
  const MESSAGE_CLOSE_DURATION_MS = 280;
  let captureHintTimeoutId = null;

  const isTypingTarget = (target) => {
    if (!(target instanceof HTMLElement)) {
      return false;
    }
    const tag = target.tagName.toLowerCase();
    return (
      tag === "input" || tag === "textarea" || tag === "select" || target.isContentEditable
    );
  };

  const anyDialogOpen = () => Array.from(document.querySelectorAll("dialog[open]")).length > 0;

  const focusFirstField = (modal) => {
    // Prefer an explicit [autofocus] hint, then editable fields, then any button.
    // Buttons come last so a header "Close" button doesn't steal focus from the title input.
    const focusTarget =
      modal.querySelector("[autofocus]") ||
      modal.querySelector(
        "input:not([type='hidden']):not([type='button']):not([type='submit']), textarea, select"
      ) ||
      modal.querySelector("button");
    if (focusTarget) {
      focusTarget.focus();
    }
  };

  const openModal = (modal, trigger) => {
    modalState.set(modal, trigger || null);
    if (!modal.open) {
      modal.showModal();
    }
    document.body.classList.add("has-modal-open");
    focusFirstField(modal);
  };

  const closeModal = (modal) => {
    if (modal.open) {
      modal.close();
    }
  };

  const registerModal = (modal) => {
    if (!(modal instanceof HTMLDialogElement) || initializedModals.has(modal)) {
      return;
    }
    initializedModals.add(modal);

    modal.addEventListener("click", (event) => {
      if (event.target === modal) {
        closeModal(modal);
      }
    });

    modal.addEventListener("close", () => {
      document.body.classList.remove("has-modal-open");
      const returnFocusId = modal.dataset.returnFocus;
      const trigger =
        modalState.get(modal) ||
        (returnFocusId ? document.getElementById(returnFocusId) : null);
      if (trigger instanceof HTMLElement) {
        trigger.focus({ preventScroll: true });
      }
    });

    modal.addEventListener("cancel", () => {
      document.body.classList.remove("has-modal-open");
    });

    if (modal.dataset.openOnLoad === "true") {
      const returnFocusId = modal.dataset.returnFocus;
      const trigger = returnFocusId ? document.getElementById(returnFocusId) : null;
      openModal(modal, trigger);
    }
  };

  const registerModals = (root) => {
    if (!root) {
      return;
    }

    if (root instanceof HTMLDialogElement && root.hasAttribute("data-modal")) {
      registerModal(root);
    }

    if (root instanceof Element || root instanceof Document) {
      root.querySelectorAll("dialog[data-modal]").forEach(registerModal);
    }
  };

  const focusInboxTarget = () => {
    if (!pendingInboxFocusReturn) {
      return;
    }

    if (document.querySelector("dialog[data-modal][open]")) {
      pendingInboxFocusReturn = null;
      return;
    }

    if (pendingInboxFocusReturn === "capture-trigger") {
      const trigger = document.getElementById("quick-capture-trigger");
      if (trigger instanceof HTMLElement) {
        trigger.focus({ preventScroll: true });
      }
    }

    if (pendingInboxFocusReturn === "selected-panel") {
      const target =
        document.querySelector("[data-inbox-selected-focus]") ||
        document.querySelector("[data-inbox-selected]");
      if (target instanceof HTMLElement) {
        if (!target.hasAttribute("tabindex")) {
          target.setAttribute("tabindex", "-1");
        }
        target.focus({ preventScroll: true });
      }
    }

    pendingInboxFocusReturn = null;
  };

  const registerHistoryTooltips = (root) => {
    if (!window.tippy || !root) {
      return;
    }

    const elements =
      root instanceof Element && root.matches(TOOLTIP_SELECTOR)
        ? [root]
        : Array.from(root.querySelectorAll?.(TOOLTIP_SELECTOR) || []);

    elements.forEach((element) => {
      if (!(element instanceof HTMLElement) || element._tippy) {
        return;
      }

      window.tippy(element, {
        allowHTML: false,
        animation: "fade",
        appendTo: () => document.body,
        arrow: true,
        delay: [90, 40],
        hideOnClick: true,
        interactive: false,
        maxWidth: 280,
        placement: "top",
        theme: "casedock-history",
        touch: true,
        trigger: "mouseenter focus click",
      });
    });
  };

  const clearMessageDismissTimer = (message) => {
    const timeoutId = messageDismissTimers.get(message);
    if (timeoutId) {
      window.clearTimeout(timeoutId);
      messageDismissTimers.delete(message);
    }
  };

  const removeMessage = (message) => {
    if (!(message instanceof HTMLElement)) {
      return;
    }

    clearMessageDismissTimer(message);
    const group = message.closest("[data-message-group]");
    message.remove();

    if (group instanceof HTMLElement && !group.querySelector(MESSAGE_SELECTOR)) {
      group.remove();
    }
  };

  const dismissMessage = (message) => {
    if (!(message instanceof HTMLElement) || message.dataset.messageState === "closing") {
      return;
    }

    clearMessageDismissTimer(message);
    message.dataset.messageState = "closing";
    message.style.height = `${message.offsetHeight}px`;

    window.requestAnimationFrame(() => {
      message.classList.remove("is-visible");
      message.classList.add("is-closing");
      message.style.height = "0px";
    });

    window.setTimeout(() => {
      removeMessage(message);
    }, MESSAGE_CLOSE_DURATION_MS);
  };

  const activateMessage = (message) => {
    if (!(message instanceof HTMLElement) || initializedMessages.has(message)) {
      return;
    }

    initializedMessages.add(message);

    window.requestAnimationFrame(() => {
      message.classList.add("is-visible");
    });

    const group = message.closest("[data-message-group]");
    const duration = Number(group?.dataset.messageDuration || 0);
    if (duration > 0) {
      message.style.setProperty("--message-duration", `${duration}ms`);
      const timeoutId = window.setTimeout(() => {
        dismissMessage(message);
      }, duration);
      messageDismissTimers.set(message, timeoutId);
    }
  };

  const registerMessages = (root) => {
    if (!root) {
      return;
    }

    const elements =
      root instanceof Element && root.matches(MESSAGE_SELECTOR)
        ? [root]
        : Array.from(root.querySelectorAll?.(MESSAGE_SELECTOR) || []);

    elements.forEach(activateMessage);
  };

  const showCaptureLandingHint = (inboxPage) => {
    if (!(inboxPage instanceof HTMLElement)) {
      return;
    }

    const destination = inboxPage.dataset.captureLandedIn;
    if (!destination) {
      return;
    }

    const target = inboxPage.querySelector(`[data-capture-destination="${destination}"]`);
    delete inboxPage.dataset.captureLandedIn;

    if (!(target instanceof HTMLElement)) {
      return;
    }

    target.classList.remove("capture-destination-hint");
    // Force a reflow so repeated captures replay the hint cleanly.
    void target.offsetWidth;
    target.classList.add("capture-destination-hint");

    if (captureHintTimeoutId) {
      window.clearTimeout(captureHintTimeoutId);
    }

    captureHintTimeoutId = window.setTimeout(() => {
      target.classList.remove("capture-destination-hint");
      captureHintTimeoutId = null;
    }, 950);
  };

  document.addEventListener("click", (event) => {
    const messageDismiss = event.target.closest("[data-message-dismiss]");
    if (messageDismiss) {
      const message = messageDismiss.closest(MESSAGE_SELECTOR);
      if (message instanceof HTMLElement) {
        event.preventDefault();
        dismissMessage(message);
      }
      return;
    }

    const trigger = event.target.closest("[data-modal-trigger]");
    if (trigger) {
      const modal = document.getElementById(trigger.dataset.modalTrigger);
      if (!(modal instanceof HTMLDialogElement)) {
        return;
      }
      event.preventDefault();
      openModal(modal, trigger);
      return;
    }

    const dismiss = event.target.closest("[data-modal-dismiss]");
    if (!dismiss) {
      return;
    }

    const modal = dismiss.closest("dialog");
    if (modal instanceof HTMLDialogElement) {
      event.preventDefault();
      closeModal(modal);
    }
  });

  document.addEventListener("submit", (event) => {
    const form = event.target.closest("[data-inbox-focus-return]");
    if (!(form instanceof HTMLElement)) {
      return;
    }
    pendingInboxFocusReturn = form.dataset.inboxFocusReturn || null;
  });

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-inbox-focus-return]");
    if (!(trigger instanceof HTMLElement)) {
      return;
    }
    pendingInboxFocusReturn = trigger.dataset.inboxFocusReturn || null;
  });

  registerModals(document);
  registerMessages(document);
  registerHistoryTooltips(document);

  document.addEventListener("keydown", (event) => {
    const shortcutsModal = document.getElementById("keyboard-shortcuts-modal");
    if (!(shortcutsModal instanceof HTMLDialogElement)) {
      return;
    }

    if (
      event.key === "c" &&
      !event.ctrlKey &&
      !event.metaKey &&
      !event.altKey &&
      !event.shiftKey &&
      !isTypingTarget(event.target) &&
      !anyDialogOpen()
    ) {
      const inboxModal = document.getElementById("capture-modal");
      const globalModal = document.getElementById("global-capture-modal");
      if (inboxModal instanceof HTMLDialogElement && !inboxModal.open) {
        event.preventDefault();
        openModal(inboxModal);
      } else if (globalModal instanceof HTMLDialogElement && !globalModal.open) {
        event.preventDefault();
        openModal(globalModal);
      } else if (!inboxModal && !globalModal) {
        window.location.href = "/inbox/capture/new/";
      }
      return;
    }

    if (
      event.key === "/" &&
      (event.ctrlKey || event.metaKey) &&
      !event.altKey &&
      !event.shiftKey
    ) {
      event.preventDefault();
      if (shortcutsModal.open) {
        closeModal(shortcutsModal);
      } else {
        openModal(shortcutsModal);
      }
      return;
    }

    if (event.key === "h" && shortcutsModal.open) {
      const helpModal = document.getElementById("page-help-modal");
      if (!(helpModal instanceof HTMLDialogElement)) {
        return;
      }
      event.preventDefault();
      closeModal(shortcutsModal);
      openModal(helpModal);
    }
  });

  if (window.htmx) {
    document.body.addEventListener("htmx:afterSwap", (event) => {
      const target = event.detail?.target;
      if (!(target instanceof HTMLElement)) {
        return;
      }

      registerMessages(target);

      const inboxPage =
        target.id === "inbox-page" ? target : document.getElementById("inbox-page");
      if (!(inboxPage instanceof HTMLElement)) {
        return;
      }

      registerModals(inboxPage);
      registerHistoryTooltips(inboxPage);
      showCaptureLandingHint(inboxPage);
      if (!document.querySelector("dialog[data-modal][open]")) {
        document.body.classList.remove("has-modal-open");
      }
      focusInboxTarget();
    });
  }
})();
