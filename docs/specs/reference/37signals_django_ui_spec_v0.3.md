# 37signals-Inspired Django Starter Kit Spec
Version: v0.3  
Audience: Codex CLI / implementation agent  
Target stack: Django templates + HTMX + Tailwind CSS  
Design reference: **Fizzy + Basecamp**  
Theme support: **Light + Dark**  
Deliverable goal: **reusable starter kit**, not one domain-specific module

---

## 1. Locked decisions

These are already decided and should be treated as requirements, not suggestions.

- Use **Tailwind CSS**
- UI copy should be in **English**
- Provide **two layout variants**:
  - Variant A: top navigation shell
  - Variant B: left sidebar + top utility bar shell
- Visual reference should be a **hybrid of Fizzy + Basecamp**
- Support **light mode and dark mode** from the beginning
- Provide **two data-presentation variants**:
  - Variant A: cards / stacked list first
  - Variant B: soft-table / structured list first
- Provide a **calm default density**
- Also include a **compact density option**
- Build a **starter kit** rather than a fully domain-specific app
- Demo/sample resource should be **ticket records**
- Command palette should be a **real working feature**
- Auth should include **basic screens plus placeholders** for reset/invite/2FA flows
- Branding should stay **neutral** and reusable across products

---

## 2. Design objective

Create a Django starter kit that captures the underlying product qualities associated with the 37signals design language, especially the overlap between Basecamp calmness and Fizzy vibrancy.

The result must feel:

- calm
- fast
- highly readable
- human
- opinionated
- colorful in a restrained way
- practical for daily work
- reusable for business software

The starter must **not** feel like:

- default Django admin
- generic Tailwind SaaS boilerplate
- a crypto dashboard
- an enterprise ERP cockpit
- a component showcase disconnected from real product screens

This is a **work tool UI**, not a marketing site.

---

## 3. Style blend: what “Fizzy + Basecamp” means

This project should combine two related but slightly different qualities.

### 3.1 From Basecamp
Adopt:

- calm information hierarchy
- strong editorial clarity
- very clear page structure
- low interface noise
- reassuring, human copy
- obvious “what matters here?” priority
- less chrome, more content

### 3.2 From Fizzy
Adopt:

- brighter accent energy
- stronger color identity in selected states and chips
- more playful but still disciplined controls
- more confident board/list objects
- slightly more vivid micro-contrast
- a feeling of directness and momentum

### 3.3 Resulting hybrid
The starter should land here:

- **structurally calm like Basecamp**
- **visually a little more lively like Fizzy**
- **never loud**
- **never sterile**

Think:

> calm product skeleton + vibrant operational details

---

## 4. Product philosophy to encode into the UI

### 4.1 Big picture first
Every screen should make the answer to these questions obvious:

1. Where am I?
2. What matters most on this page?
3. What can I do right now?
4. What changed or needs attention?

### 4.2 Quiet interface, strong content
Prefer hierarchy through:

- spacing
- alignment
- typography
- surface contrast
- selective accent color

Do not rely on:

- giant shadows
- thick dividers everywhere
- many KPI cards by default
- heavy chromed panels
- too many visible actions in the first layer

### 4.3 Layered interaction
Prefer revealing detail progressively.

Prefer:

- drawers
- trays
- dropdown panels
- inline expansion
- partial HTMX updates
- lightweight overlays

Use full-page transitions only when context actually changes.

### 4.4 Opinionated defaults
The starter kit should guide product teams toward sane defaults.
Do not over-design for extreme configurability.
Choose one good pattern first, then expose alternatives only where necessary.

---

## 5. Core visual language

### 5.1 General mood
The app should feel:

- airy but not sparse
- compact enough for work
- text-led
- subtly tactile
- slightly editorial
- gently handcrafted
- friendly without being cute

### 5.2 Shape language
Use shape meaningfully.

- primary CTAs: pill or near-pill
- secondary actions: soft rounded rectangle or pill
- inputs: rounded but not balloon-like
- panels/cards: softly rounded rectangles
- chips/tags/filters: pill
- popovers/drawers: soft rounded corners, slightly more elevated

### 5.3 Density model
The starter must support **two density modes**:

#### Calm (default)
Use this as the shipped default.

- more breathing room
- slightly taller list rows
- more generous page spacing
- better for long-form reading, notes, and all-day use

#### Compact (optional)
Provide a denser version without turning the UI into ERP chrome.

- reduced vertical padding
- more rows visible on screen
- tighter list/table rhythm
- same hierarchy and readability principles
- no tiny text
- no cramped controls

Implementation recommendation:
Use a `data-density="calm|compact"` attribute on `html` or `body` and drive spacing/radius/row-height adjustments with semantic CSS variables.

---

## 6. Color system

Important: this is inspiration-driven and should not aim to clone another product exactly.
Implement colors as **semantic tokens** backed by CSS variables.

## 6.1 Color intent

- most of the interface should be neutral
- blue should be the primary action/link/navigation accent
- pale selection fills should help orientation
- colorful states may appear in chips, boards, highlights, empty states, and selected views
- purple and pink may exist as expressive secondary accents, but should not become the default CTA language
- branding must remain neutral enough to re-theme later without rewriting components

## 6.2 Light theme tokens

```css
:root {
  --bg-app: #f7f8fa;
  --bg-canvas: #ffffff;
  --bg-panel: #ffffff;
  --bg-elevated: #ffffff;
  --bg-subtle: #f3f5f7;
  --bg-selected: #e9f2ff;
  --bg-selected-strong: #dbe9ff;
  --bg-soft-blue: #f1f7ff;
  --bg-soft-yellow: #fff7df;
  --bg-soft-green: #edf9f0;
  --bg-soft-red: #fff0ea;
  --bg-soft-purple: #f5efff;

  --text-primary: #17233c;
  --text-secondary: #404856;
  --text-muted: #70757d;
  --text-faint: #8f9297;
  --text-on-accent: #ffffff;

  --border-subtle: #e3e5e8;
  --border-default: #ccd2d9;
  --border-strong: #b4bcc6;

  --accent-primary: #2d71e5;
  --accent-primary-hover: #2563d4;
  --accent-primary-active: #1f57be;
  --accent-link: #2d71e5;
  --accent-link-hover: #215fcb;

  --accent-purple: #9c5de5;
  --accent-pink: #e96cc5;
  --accent-gold: #f2c94c;
  --accent-green: #1f8f4d;
  --accent-red: #d4572a;

  --focus-ring: rgba(45, 113, 229, 0.35);
  --shadow-soft: 0 1px 2px rgba(16, 24, 40, 0.04), 0 8px 24px rgba(16, 24, 40, 0.06);
  --shadow-pop: 0 10px 30px rgba(16, 24, 40, 0.10);
}
```

## 6.3 Dark theme tokens

```css
.dark {
  --bg-app: #0d141b;
  --bg-canvas: #101922;
  --bg-panel: #13202a;
  --bg-elevated: #182532;
  --bg-subtle: #0f1a22;
  --bg-selected: #17314d;
  --bg-selected-strong: #21466e;
  --bg-soft-blue: #122335;
  --bg-soft-yellow: #2b2513;
  --bg-soft-green: #11281b;
  --bg-soft-red: #2c1813;
  --bg-soft-purple: #23192f;

  --text-primary: #f3f6fb;
  --text-secondary: #d4dce6;
  --text-muted: #a6afbb;
  --text-faint: #8591a1;
  --text-on-accent: #ffffff;

  --border-subtle: #213140;
  --border-default: #2b3f52;
  --border-strong: #3a536a;

  --accent-primary: #72adfb;
  --accent-primary-hover: #5b9ef7;
  --accent-primary-active: #4287e3;
  --accent-link: #7ab2ff;
  --accent-link-hover: #94c0ff;

  --accent-purple: #be90ff;
  --accent-pink: #ff93da;
  --accent-gold: #f7d96b;
  --accent-green: #78c98d;
  --accent-red: #f08a64;

  --focus-ring: rgba(122, 178, 255, 0.35);
  --shadow-soft: 0 1px 2px rgba(0,0,0,0.28), 0 8px 24px rgba(0,0,0,0.24);
  --shadow-pop: 0 14px 34px rgba(0,0,0,0.36);
}
```

## 6.4 Semantic aliases required

Do not scatter raw token names everywhere in components.
Create semantic aliases like:

- `--surface-page`
- `--surface-panel`
- `--surface-elevated`
- `--surface-subtle`
- `--surface-selected`
- `--text-primary`
- `--text-secondary`
- `--text-muted`
- `--border-subtle`
- `--border-default`
- `--action-primary-bg`
- `--action-primary-text`
- `--action-secondary-bg`
- `--action-secondary-text`
- `--status-success`
- `--status-warning`
- `--status-danger`
- `--focus-ring`

Map design tokens to semantic usage in one place.

## 6.5 Color usage rules

1. Large surfaces should remain mostly neutral.
2. Accent color should guide interaction, not flood the page.
3. Selected states must be gentle but obvious.
4. Status colors should be readable but not alarmist.
5. Board columns, chips, and states may be slightly more colorful than forms and tables.
6. Dark mode should keep contrast strong without becoming neon.

---

## 7. Typography

### 7.1 Font direction
Primary recommendation:

- `Inter`
- fallback to system sans stack

Suggested stack:

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

### 7.2 Type scale
Use a practical, app-friendly scale.

- `text-xs`: 12px
- `text-sm`: 14px
- `text-base`: 16px
- `text-md`: 17px
- `text-lg`: 20px
- `text-xl`: 24px
- `text-2xl`: 32px

### 7.3 Typography behavior

- body text must remain comfortably readable
- metadata must remain legible, not tiny
- headings should be confident, not oversized
- all-caps should be rare
- labels should sound like product language, not raw form schema

### 7.4 Text tone
Hierarchy should come from:

- size
- weight
- spacing
- color contrast

Not from:

- over-bold everything
- extreme tracking
- aggressive uppercase labeling

---

## 8. Spacing, radius, border, shadow

### 8.1 Spacing scale
Use a 4px base rhythm, but favor these steps in visible layouts:

- 4
- 8
- 12
- 16
- 20
- 24
- 32
- 40

### 8.2 Radius scale
Recommended defaults:

- `--radius-xs`: 8px
- `--radius-sm`: 10px
- `--radius-md`: 14px
- `--radius-lg`: 18px
- `--radius-xl`: 22px
- `--radius-pill`: 999px

Usage:

- inputs: 10px
- panels: 18px
- cards: 16px
- menus/popovers: 18px–22px
- primary buttons: pill
- chips: pill

### 8.3 Borders
Default to subtle 1px borders.
Use borders for structure more often than shadows.

### 8.4 Shadows
Shadows should be soft and selective.
Use them primarily for:

- popovers
- dropdowns
- drawers
- dialogs
- floating action clusters

Avoid making all panels look like floating clouds.

---

## 9. Tailwind implementation strategy

Tailwind should be the delivery mechanism, not the visual identity.

### 9.1 Rules

- use CSS variables for theme tokens
- map variables into Tailwind utilities or component classes
- avoid default Tailwind gray/blue feel
- create reusable semantic component classes in `@layer components`
- prefer templates + partials over component libraries that impose a foreign aesthetic

### 9.2 Tailwind config direction
The starter should expose semantic names for:

- colors
- radius
- boxShadow
- spacing where helpful

Recommended approach:

- keep raw CSS variables in `app.css`
- expose them through Tailwind utility-friendly aliases
- use utility classes for layout and spacing
- use semantic component classes for recurring objects like buttons, panels, chips, inputs, nav items

### 9.3 Required component classes
At minimum define:

- `.btn`
- `.btn-primary`
- `.btn-secondary`
- `.btn-ghost`
- `.btn-danger`
- `.input`
- `.textarea`
- `.select`
- `.search-input`
- `.panel`
- `.card-soft`
- `.chip`
- `.chip-active`
- `.empty-state`
- `.nav-item`
- `.nav-item-active`
- `.table-soft`
- `.drawer`
- `.popover-panel`
- `.page-shell`
- `.page-header`
- `.section-title`
- `.density-toggle`
- `.command-palette`
- `.auth-placeholder-panel`

### 9.4 Theme switching
Implement theme switching with class-based dark mode.

Requirements:

- use `html.dark` or `body.dark`
- starter should include a theme toggle component
- persist preference in localStorage
- respect system preference on first load if no saved preference exists
- avoid flash of incorrect theme if possible

### 9.5 Density switching
Implement calm/compact density switching.

Requirements:

- use `data-density="calm|compact"` on `html` or `body`
- include a density toggle in settings and optionally the command palette
- persist preference in localStorage
- ensure both list variants and form layouts respond correctly
- compact mode must not reduce accessibility or touch targets excessively

---

## 10. Layout variants

The starter must provide **two shell variants**.
Both should share the same tokens and components.

## 10.1 Variant A: Top Navigation Shell
Best for:

- compact internal tools
- products where primary sections are limited
- products that benefit from a lighter, less “admin” feeling

### Structure

- slim top bar
- left side: product mark, workspace switcher or section tabs
- center or left-center: search, depending on app size
- right side: command palette trigger, utility actions, theme toggle, notifications, account menu
- page content below in a centered max-width container

### Feel
This variant should feel closest to Basecamp.
It should be the calmer, lighter, more editorial option.

### Use cases

- overview screens
- dashboard
- lightweight CRM
- project/work pages
- knowledge/process tools

## 10.2 Variant B: Sidebar + Top Utility Shell
Best for:

- back-office apps with more sections
- operations tools
- products with many resource groups
- apps where users switch between many list/detail pages

### Structure

- fixed or sticky left sidebar
- compact top utility bar inside main content area
- sidebar contains primary navigation only
- top utility bar contains search, command palette trigger, quick actions, theme toggle, user menu
- content region uses strong page headers and section blocks

### Feel
This variant should feel slightly more operational and closer to Fizzy when paired with lively chips, selection states, and boards.

### Use cases

- inventory systems
- CRM/backoffice
- admin tools
- internal operations software

## 10.3 Shared shell rules
Both variants must:

- avoid excessive chrome
- keep search easy to reach
- keep primary actions obvious
- support small-screen collapse
- keep content as the hero, not the container architecture

---

## 11. Data presentation variants

The starter must provide **two main patterns** for resource/index pages.

## 11.1 Variant A: Cards / Stacked List First
Best for:

- tickets with richer context
- conversations
- requests with notes
- records where metadata matters more than dense comparison
- mobile-friendly pages

### Characteristics

- each item has title, metadata, optional tags/status, optional assignee, optional action menu
- stronger spacing between records
- more human and readable
- easier to enrich with notes, avatars, activity, secondary copy

### Feel
This should be the more Basecamp-like mode.

## 11.2 Variant B: Soft Table / Structured List First
Best for:

- ticket queues
- triage views
- SLA-oriented worklists
- resources where quick scanning and comparison matter

### Characteristics

- table-like alignment but softened visually
- reduced grid harshness
- slightly taller rows than enterprise defaults
- subtle row hover and selected states
- row click may open side detail tray
- actions should remain sparse

### Feel
This should be more operational, but still calm.
It should not look like a default admin table.

## 11.3 Shared rules for both variants

- search and filters live above the content
- primary CTA should be visible without being over-dominant
- empty states must feel intentional
- bulk actions should be restrained and contextual
- optional detail tray should work with both variants

---

## 12. Starter kit information architecture

The starter should be generic enough to reuse across products, but real enough to demonstrate usage.

### 12.1 Recommended starter pages
Generate these demo pages:

1. dashboard
2. ticket index in card mode
3. ticket index in soft-table mode
4. ticket detail page
5. create/edit form page
6. settings/profile page
7. notifications/activity page
8. sign-in page
9. reset password placeholder page
10. invite user placeholder page
11. 2FA setup placeholder page
12. empty-state examples page
13. component playground page
14. command palette result view or demo page

### 12.2 Demo domain for samples
Use **ticket records** as the demo resource.

Suggested fields:

- ticket number
- title
- requester
- assignee
- priority
- status
- channel
- created at
- updated at
- due at
- tags
- short summary

This demo domain should remain generic enough to repurpose for requests, issues, tasks, or support workflows.

---

## 13. Required component inventory

Codex should generate reusable partials/components for:

### 13.1 Global shell

- app shell wrapper
- top navigation shell
- sidebar shell
- utility bar
- page container
- page header
- breadcrumb or back link pattern

### 13.2 Actions

- primary button
- secondary button
- ghost button
- icon button
- split button or action menu trigger
- destructive confirmation button

### 13.3 Form primitives

- text input
- textarea
- select
- search input
- checkbox
- radio group
- toggle switch
- inline help text
- validation error block
- field group wrapper
- sticky action row

### 13.4 Content primitives

- panel
- soft card
- metadata row
- chip/tag
- avatar stub
- status pill
- priority pill
- stat block
- activity item
- empty state
- flash message

### 13.5 Layered UI

- dropdown menu
- popover panel
- right-side drawer
- modal confirmation
- command palette
- command result group
- quick action item

### 13.6 Data views

- stacked list item
- card grid item
- soft table
- filter chip row
- sort control
- pagination block

### 13.7 Auth placeholders

- reset password request placeholder
- reset password confirm placeholder
- invite acceptance placeholder
- 2FA setup placeholder
- 2FA challenge placeholder

---

## 14. Interaction rules

### 14.1 Motion
Motion should support orientation.

Recommended:

- 100ms–180ms transitions
- fade and short slide for overlays
- background, border, and shadow transitions
- no theatrical movement

### 14.2 HTMX preference
The starter should demonstrate HTMX for:

- search/filter partial refresh
- inline status update
- drawer-loaded detail preview
- form validation fragment updates
- flash messages after partial actions
- command palette result loading
- ticket list density-aware refresh

### 14.3 Keyboard support
Required:

- strong visible focus state
- logical tab order
- ESC closes popover/drawer/command palette where relevant
- Enter submits obvious forms
- `cmd/ctrl+k` opens the command palette
- slash may focus search when appropriate

### 14.4 Selection and state visibility
Selected state must not rely on color alone.
Combine:

- background shift
- border emphasis
- font weight or marker
- icon/check when appropriate

---

## 15. Command palette requirements

The command palette is a **real feature**, not a visual stub.

### 15.1 Use cases
It should support at least:

- global navigation between starter pages
- quick access to ticket records
- action commands such as “New ticket”, “Go to settings”, “Toggle theme”, “Switch density”
- lightweight result grouping

### 15.2 Interaction model

- open with `cmd/ctrl+k`
- close with ESC
- searchable input at top
- grouped results below
- keyboard navigation with arrow keys
- highlighted active result
- Enter executes selected result
- empty state when nothing matches

### 15.3 Data strategy
Implementation may start with a local JS index or server-assisted HTMX results.
Keep architecture open for later replacement with app-specific search.

### 15.4 Visual rules
The command palette should feel:

- elevated but not glossy
- compact but readable
- close to app language, not a third-party widget
- aligned with the same panel, border, radius, and focus tokens as the rest of the UI

---

## 16. Content and copy style

Copy should feel:

- direct
- calm
- human
- useful
- not over-explained

Use product language like:

- “No tickets yet.”
- “Create your first ticket.”
- “Search by title, requester, or tag.”
- “You can change this later.”
- “Saved.”
- “Couldn’t save your changes.”

Avoid:

- jargon-heavy system text
- hype language
- “unlock”, “optimize”, “supercharge” style copy
- lifeless form-schema phrasing

---

## 17. Accessibility requirements

Non-negotiable:

- WCAG AA contrast for key text and controls
- visible focus rings
- labels for all form controls
- hover-only actions must have keyboard/touch alternatives
- errors must be textual, not color-only
- selected state must be color-plus-other-signal
- drawers, modals, menus, and command palette must support keyboard escape and focus management

---

## 18. Django project structure recommendation

```text
project/
  config/
  apps/
    core/
      templates/
        layouts/
          app_topnav.html
          app_sidebar.html
          auth.html
        partials/
          header_topnav.html
          header_sidebar.html
          utility_bar.html
          page_header.html
          flash.html
          empty_state.html
          pagination.html
          filters_row.html
          theme_toggle.html
          density_toggle.html
          command_palette.html
        components/
          buttons/
            primary.html
            secondary.html
            ghost.html
            icon.html
          forms/
            input.html
            textarea.html
            select.html
            checkbox.html
            field_group.html
          data/
            ticket_card.html
            ticket_list_item.html
            ticket_soft_table.html
            status_pill.html
            priority_pill.html
            chip.html
          overlays/
            drawer.html
            popover.html
            modal_confirm.html
            command_palette.html
          auth/
            sign_in_panel.html
            reset_placeholder.html
            invite_placeholder.html
            two_factor_placeholder.html
      static/
        core/
          css/
            app.css
          js/
            theme.js
            density.js
            command_palette.js
            ui.js
      views/
      urls/
      templatetags/
  templates/
    dashboard/
    tickets/
    settings/
    auth/
    command_palette/
```

---

## 19. Tailwind + CSS architecture recommendation

All reusable styling should live in a coherent structure.

### 19.1 `app.css` sections

1. theme tokens
2. density tokens
3. base element styles
4. typography defaults
5. layout objects
6. component classes
7. utility extensions
8. dark mode overrides

### 19.2 Example organization

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root { /* theme + density tokens */ }
  .dark { /* dark tokens */ }
  [data-density="compact"] { /* compact overrides */ }
  html, body { /* global base */ }
}

@layer components {
  .btn { /* shared */ }
  .btn-primary { /* shared */ }
  .panel { /* shared */ }
  .input { /* shared */ }
  .table-soft { /* shared */ }
  .command-palette { /* shared */ }
}
```

### 19.3 Important implementation note
Do not force everything into one giant utility soup inside templates.
For repeatable patterns, use component classes.

---

## 20. Starter screen recipes

## 20.1 Dashboard
Show:

- page title and short context line
- items needing attention
- recent activity
- upcoming deadlines
- shortcuts to create/open common records

Avoid dashboard KPI overload.

## 20.2 Ticket index (cards)
Show:

- title + context line
- search + filters + sort + primary CTA
- stacked or card-based ticket records
- optional right-side detail preview drawer

## 20.3 Ticket index (soft table)
Show:

- same header controls
- softened table with restrained row actions
- row selection and quick detail opening

## 20.4 Ticket detail page
Show:

- back link or breadcrumb
- strong title
- ticket meta row
- main action group
- summary/notes/history sections
- optional side activity rail or drawer

## 20.5 Form page
Show:

- compact intro
- grouped fields
- calm validation
- sticky save/cancel area when form is long
- no giant wizard unless explicitly needed

## 20.6 Settings page
Should feel clean and not over-framed.
Use grouped sections and simple headings.
Include theme and density preferences.

## 20.7 Auth placeholder pages
These should look intentionally designed, not like dead-end placeholders.
Explain that the flow is scaffolded and ready for later domain logic.

## 20.8 Command palette
Demonstrate real navigation and action execution from keyboard and mouse.

---

## 21. Required starter deliverables

Codex should generate all of the following:

1. Tailwind-integrated Django starter setup
2. semantic token system for light/dark themes
3. calm/compact density system
4. two layout shells
5. two data presentation variants
6. reusable partial/component library
7. ticket-based sample pages demonstrating all patterns
8. theme toggle with persistence
9. density toggle with persistence
10. HTMX examples for partial updates
11. real working command palette
12. auth placeholders for reset/invite/2FA
13. README with design system explanation
14. concise agent prompt for future extension work

---

## 22. Definition of done

The starter is successful only if all of the following are true:

- it clearly does not look like default Django admin
- it clearly does not look like stock Tailwind UI
- topnav and sidebar variants both work
- card-first and soft-table views both work
- calm and compact density both work
- dark mode feels designed, not auto-inverted
- the app feels calm, readable, and slightly lively
- primary buttons feel intentional and tactile
- forms are pleasant to use
- empty states feel designed
- the command palette works with keyboard and mouse
- at least one drawer/popover/partial update flow exists
- auth placeholder pages look cohesive
- the codebase is reusable rather than tightly coupled to one resource

---

## 23. Implementation order for Codex

Follow this order:

1. set up Django + Tailwind integration
2. create tokenized light/dark theme foundation
3. create calm/compact density foundation
4. implement base typography and spacing rules
5. build reusable buttons, inputs, panels, chips, empty states
6. implement topnav shell
7. implement sidebar shell
8. implement card/stacked-list ticket page
9. implement soft-table ticket page
10. implement detail + form + settings pages
11. add theme toggle and persistence
12. add density toggle and persistence
13. implement command palette
14. add auth placeholder screens
15. add HTMX progressive interactions
16. write README and extension guide

---

## 24. Primary prompt for Codex CLI

Use this prompt as the main build brief.

### Codex Prompt
Build a reusable Django starter kit using Django templates, HTMX, and Tailwind CSS. The UI should be inspired by the underlying product design qualities of 37signals, specifically a hybrid of Basecamp and Fizzy. Do not copy trademarks, logos, or exact screens. Recreate the qualities instead: calm structure, strong readability, low interface noise, human product copy, layered interactions, pill and soft-rounded controls, restrained but expressive color, semantic design tokens, subtle borders, and light-but-confident surfaces.

Hard requirements:
- use Tailwind CSS
- use English UI copy
- support light and dark themes from the start
- support two density modes:
  1. calm (default)
  2. compact (optional)
- provide two app shell variants:
  1. top navigation shell
  2. left sidebar with top utility bar shell
- provide two resource/index variants:
  1. cards/stacked-list first
  2. soft-table first
- build a reusable starter kit rather than one domain-specific module
- use ticket records as the sample domain
- use Django templates first
- use HTMX for partial updates
- keep JavaScript minimal
- create reusable partials/components for buttons, forms, panels, cards, chips, empty states, soft tables, popovers, drawers, and auth placeholders
- include a real working command palette with keyboard support
- include accessible focus states, keyboard support, and good empty/error states
- include placeholder screens for reset password, invite flow, and 2FA
- keep branding neutral and reusable

Visual direction:
- mostly neutral surfaces
- dark ink text in light mode
- strong readable text in dark mode
- blue as primary action/link accent
- occasional purple/pink/gold accents for expressive supporting states
- pill primary buttons
- softly rounded panels and cards
- subtle borders
- soft shadows only for floating layers
- calm page composition
- no generic admin look
- no dashboard clutter

Starter pages to generate:
- dashboard
- card-based ticket index
- soft-table ticket index
- ticket detail page
- create/edit form page
- settings page
- sign-in page
- reset password placeholder page
- invite placeholder page
- 2FA placeholder page
- empty-state examples page
- component playground page

Deliverables:
1. Django/Tailwind starter setup
2. token-based theme system
3. density system
4. two layout shells
5. two data-view variants
6. reusable partial/component library
7. sample ticket pages
8. theme toggle with persistence
9. density toggle with persistence
10. working command palette
11. HTMX demo interactions
12. README explaining architecture, tokens, components, and extension rules

Implementation style:
- prefer semantic component classes over giant repetitive utility strings
- prefer server-rendered HTML with small HTMX enhancements
- prioritize clarity, calmness, and reusability
- when in doubt, choose simpler, calmer, and more readable

---

## 25. Short prompt version for repeated future use

Use this when you do not want to paste the full brief.

### Short Codex Prompt
Create a reusable Django starter kit with Tailwind + HTMX inspired by a Basecamp/Fizzy design hybrid: calm structure, readable typography, semantic tokens, neutral branding, light/dark themes, calm default density with compact option, pill primary buttons, soft panels, subtle borders, layered UI, two shells (topnav and sidebar), and two ticket index modes (cards and soft-table). Build a real command palette, auth placeholders, reusable partials, and starter pages. Avoid generic Tailwind SaaS aesthetics and avoid default admin look.

---

## 26. Optional future extensions

These are not required in v0.3, but the architecture should remain compatible with them.

- workspace switcher
- multi-project navigation
- activity inbox
- inline comments
- attachments/media rail
- saved views
- ticket SLA widgets
- richer quick filters
- mobile-specific command actions
- per-user density and theme settings stored server-side

---

## 27. Final instruction to the agent

When uncertain, choose:

- calmer over louder
- clearer over cleverer
- more readable over more decorative
- fewer visible actions over more clutter
- semantic reuse over one-off styling
- layered context over disruptive navigation
- practical product rhythm over component-demo aesthetics

The starter should feel like a product someone could work in every day.
