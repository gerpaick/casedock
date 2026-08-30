# Board — Your Daily Starting Point

When you open casedock, the first thing you see is the Board. It is not a dashboard full of
charts. It is not a list of everything you need to do. It is **your view of today** — calm,
intentional, and free of noise.

## What is on the Board

The Board has three sections. That's it. Not five, not ten. Three.

### 1. Daily Focus

The most important thing on the page. Your work for today.

**One main Case (Main)** plus, optionally, **two supporting Cases (Secondary)**.

Example: You sit down to work in the morning. You know that today you want to:

- Mainly: fix the user login bug
- If there is time: improve the API documentation
- If there is time: reply to a client's email about an integration

You set "Fix login bug" as Main and the other two as Secondary. Now, whenever you open
casedock, you immediately know where you left off. You do not have to think, "What was I
supposed to be doing?" — the Board reminds you.

**If you have not set a focus**, you see a calm message: "Nothing has the front yet. Pick one
main Case and, if useful, up to two secondary Cases." No `alert.png`, no red exclamation mark.
Just information.

Why a maximum of 1 + 2? Because focus means attention. If everything is important, nothing is
important. Three Cases are the most you can realistically keep in mind during one day.

### 2. Stale Cases (items that need a decision)

This is a **gentle reminder**, not a complaint.

If you have an active Case that you have not touched for seven days (by default), the Board
reminds you about it. Not with a list of alarms or a notification — just one card on the Board
that says "Untouched for 11 days" and offers three options:

- **Done** — close it because it is finished. We often forget to close things that already work.
- **Move to waiting** — move it because you are waiting for someone or something. Do not let it
  clutter the active list.
- **Still active** — "I know about it; I am working on it." But note that you can select this only
  three times. After that, you must make a decision.

Example: You have a Case called "Refactor settings page." It was last edited two weeks ago, so
the Board shows it to you. You select "Still active" because you genuinely want to return to it.
A week later, the Board asks again. You select "Still active" a second time, then a third time
the following week. There is no fourth time. The Board says, "Okay, now you need to decide —
are you doing this, waiting for something, or is it already done?"

Why not block the user? Because hard blocks work worse than reminders for people with ADHD. If
you block someone, they may avoid the app instead of taking action. It is better to offer a
gentle reminder and a way forward.

Cases in today's focus do not appear as stale — which makes sense, because you are actively
working on them.

### 3. Stats + Links

At the bottom of the Board, one row shows three numbers and two links:

```
4 active  ·  3 waiting  ·  2 closed this week

[See all active →]    [See waiting →]
```

This is an overview of the situation. You can see how much is on your plate without going into
detail. Select "See all active" to open the full list of active Cases, or "See waiting" to see
what is waiting.

Why not show the full list on the Board? Because the Board is about "what I am doing today," not
"everything I need to do." Full lists live in separate views — just as the Inbox has its own
screen, so do Active and Waiting.

---

## Focus transition prompt

One more thing can appear on the Board, but only at a specific moment.

When you change the main focus to a new Case and the previous Case has not been edited since you
focused on it, the Board asks what should happen to it:

```
"Fix login bug" hasn't been updated since you focused on it.
[Done]  [Move to waiting]  [Still working]
```

This is a natural moment to ask: you are changing priorities, so you are already thinking about
what mattered before and what matters now. It is not an interruption; it makes use of the
moment.

Why does this work? Because we often forget to close things. When you set a new focus, the app
catches the moment and asks. You do not have to remember to close the previous Case — the app
reminds you.

---

## What is NOT on the Board (and why)

**The full list of active Cases** — it lives in a separate view (`/active/`). The Board shows only
the focus and Cases that need attention (stale). Select the link when you want to review
everything.

**The full list of waiting Cases** — it has a separate view (`/waiting/`). It shows only titles
and next steps, with no actions, because there is nothing to do with waiting items except check
whether anything has changed.

**Inbox** — the Inbox has its own screen. The Board only shows its count in the top navigation.
Intake and work remain separate.

**Closed Cases** — included in the statistics ("2 closed this week") but not displayed. Done is
done.

---

## How to use the Board each day

**Morning:**

1. Open casedock.
2. See your focus and know where you stand.
3. If the Board asks about old Cases, make a quick decision (five seconds).
4. Start working.

**During the day:**

1. Switching between Cases? Change the focus. The Board asks what to do with the previous one.
2. Open the Board to resume work and see what is set for today.

**In the evening or the next morning:**

1. Close the Cases you have finished.
2. Move blocked items to Waiting.
3. Set a new focus for tomorrow.

---

## For the curious — how it works technically

- **Stale detection**: A Case is "stale" if it is active and has not been edited for seven or
  more days (`CASEDOCK_STALE_PERIOD_DAYS`). This is determined from `updated_at`, but "Still
  active" acknowledgments do not update that field (we use `QuerySet.update()` to bypass
  `auto_now`).
- **Stale exclusion**: Cases in today's focus are not shown as stale.
- **Ack limit**: A maximum of three "Still active" acknowledgments
  (`CASEDOCK_STALE_ACK_LIMIT`). After that, only Done and Waiting remain available.
- **Transition prompt**: Appears only when you change the main focus and the previous Case has
  not been edited since the focus was set (we compare `Case.updated_at` with
  `FocusAssignment.created_at`).
- **HTMX**: All actions (stale resolution and focus actions) work without reloading the page —
  HTMX swaps the entire `#board-page`.
