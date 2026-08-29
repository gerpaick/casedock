# 37signals-Inspired Django Starter Kit Spec
Version: v0.2  
Audience: Codex CLI / implementation agent  
Target stack: Django templates + HTMX + Tailwind CSS  
Design reference: **Fizzy + Basecamp**  
Theme support: **Light + Dark**  
Deliverable goal: **reusable starter kit**, not one domain-specific module

---

## 1. Locked decisions

These are already decided and should be treated as requirements, not suggestions.

- Use **Tailwind CSS**
- Provide **two layout variants**:
  - Variant A: top navigation shell
  - Variant B: left sidebar + top utility bar shell
- Visual reference should be a **hybrid of Fizzy + Basecamp**
- Support **light mode and dark mode** from the beginning
- Provide **two content-density / data-presentation variants**:
  - Variant A: cards / stacked list first
  - Variant B: soft-table / structured list first
- Build a **starter kit** rather than a fully domain-specific app

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

### 5.3 Density rules
Target **comfortable compactness**.

- denser than a marketing page
- calmer and more breathable than most back-office apps
- suitable for all-day use on a laptop

Default rhythm should feel efficient, not cramped.

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

### 9.4 Theme switching
Implement theme switching with class-based dark mode.

Requirements:

- use `html.dark` or `body.dark`
- starter should include a theme toggle component
- persist preference in localStorage
- respect system preference on first load if no saved preference exists
- avoid flash of incorrect theme if possible

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
- right side: utility actions, theme toggle, notifications, account menu
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
- top utility bar contains search, quick actions, theme toggle, user menu
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

- tasks
- projects
- contacts with notes/context
- records where metadata matters more than dense comparison
- mobile-friendly pages

### Characteristics

- each item has title, metadata, optional tags/status, optional action menu
- stronger spacing between records
- more human and readable
- easier to enrich with notes, avatars, activity, secondary copy

### Feel
This should be the more Basecamp-like mode.

## 11.2 Variant B: Soft Table / Structured List First
Best for:

- orders
- invoices
- inventory items
- tickets
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
2. resource index in card mode
3. resource index in soft-table mode
4. detail page
5. create/edit form page
6. settings/profile page
7. notifications/activity sample page
8. sign-in page
9. empty-state examples page
10. component playground page

### 12.2 Demo domain for samples
Use a neutral sample resource such as:

- Projects
- Tasks
- Clients
- Requests

Do not hard-code a niche business domain into the starter.

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
- stat block
- activity item
- empty state
- flash message

### 13.5 Layered UI

- dropdown menu
- popover panel
- right-side drawer
- modal confirmation
- command palette stub

### 13.6 Data views

- stacked list item
- card grid item
- soft table
- filter chip row
- sort control
- pagination block

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

### 14.3 Keyboard support
Required:

- strong visible focus state
- logical tab order
- ESC closes popover/drawer where relevant
- Enter submits obvious forms
- optional `cmd/ctrl+k` command palette stub
- slash-to-focus-search if appropriate

### 14.4 Selection and state visibility
Selected state must not rely on color alone.
Combine:

- background shift
- border emphasis
- font weight or marker
- icon/check when appropriate

---

## 15. Content and copy style

Copy should feel:

- direct
- calm
- human
- useful
- not over-explained

Use product language like:

- “Nothing here yet.”
- “Create your first project.”
- “Search by title or tag.”
- “You can change this later.”
- “Saved.”
- “Couldn’t save your changes.”

Avoid:

- jargon-heavy system text
- hype language
- “unlock”, “optimize”, “supercharge” style copy
- lifeless form-schema phrasing

---

## 16. Accessibility requirements

Non-negotiable:

- WCAG AA contrast for key text and controls
- visible focus rings
- labels for all form controls
- hover-only actions must have keyboard/touch alternatives
- errors must be textual, not color-only
- selected state must be color-plus-other-signal
- drawers, modals, and menus must support keyboard escape and focus management

---

## 17. Django project structure recommendation

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
          command_palette_stub.html
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
            card_item.html
            list_item.html
            soft_table.html
            status_pill.html
            chip.html
          overlays/
            drawer.html
            popover.html
            modal_confirm.html
      static/
        core/
          css/
            app.css
          js/
            theme.js
            ui.js
      views/
      urls/
      templatetags/
  templates/
    dashboard/
    demo_resources/
    settings/
    auth/
```

---

## 18. Tailwind + CSS architecture recommendation

All reusable styling should live in a coherent structure.

### 18.1 `app.css` sections

1. theme tokens
2. base element styles
3. typography defaults
4. layout objects
5. component classes
6. utility extensions
7. dark mode overrides

### 18.2 Example organization

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root { /* tokens */ }
  .dark { /* dark tokens */ }
  html, body { /* global base */ }
}

@layer components {
  .btn { /* shared */ }
  .btn-primary { /* shared */ }
  .panel { /* shared */ }
  .input { /* shared */ }
  .table-soft { /* shared */ }
}
```

### 18.3 Important implementation note
Do not force everything into one giant utility soup inside templates.
For repeatable patterns, use component classes.

---

## 19. Starter screen recipes

## 19.1 Dashboard
Show:

- page title and short context line
- items needing attention
- recent activity
- upcoming tasks/events or deadlines
- shortcuts to create/open common resources

Avoid dashboard KPI overload.

## 19.2 Resource index (cards)
Show:

- title + context line
- search + filters + sort + primary CTA
- stacked or card-based records
- optional right-side detail preview drawer

## 19.3 Resource index (soft table)
Show:

- same header controls
- softened table with restrained row actions
- row selection and quick detail opening

## 19.4 Detail page
Show:

- back link or breadcrumb
- strong title
- metadata row
- main action group
- content sections/panels
- optional side notes/activity rail or drawer

## 19.5 Form page
Show:

- compact intro
- grouped fields
- calm validation
- sticky save/cancel area when form is long
- no giant wizard unless explicitly needed

## 19.6 Settings page
Should feel clean and not over-framed.
Use grouped sections and simple headings.

---

## 20. Required starter deliverables

Codex should generate all of the following:

1. Tailwind-integrated Django starter setup
2. semantic token system for light/dark themes
3. two layout shells
4. two data presentation variants
5. reusable partial/component library
6. sample pages demonstrating all patterns
7. theme toggle with persistence
8. HTMX examples for partial updates
9. README with design system explanation
10. concise agent prompt for future extension work

---

## 21. Definition of done

The starter is successful only if all of the following are true:

- it clearly does not look like default Django admin
- it clearly does not look like stock Tailwind UI
- topnav and sidebar variants both work
- card-first and soft-table views both work
- dark mode feels designed, not auto-inverted
- the app feels calm, readable, and slightly lively
- primary buttons feel intentional and tactile
- forms are pleasant to use
- empty states feel designed
- at least one drawer/popover/partial update flow exists
- the codebase is reusable rather than tightly coupled to one resource

---

## 22. Implementation order for Codex

Follow this order:

1. set up Django + Tailwind integration
2. create tokenized light/dark theme foundation
3. implement base typography and spacing rules
4. build reusable buttons, inputs, panels, chips, empty states
5. implement topnav shell
6. implement sidebar shell
7. implement card/staked-list resource page
8. implement soft-table resource page
9. implement detail + form + settings pages
10. add theme toggle and persistence
11. add HTMX progressive interactions
12. write README and extension guide

---

## 23. Primary prompt for Codex CLI

Use this prompt as the main build brief.

### Codex Prompt
Build a reusable Django starter kit using Django templates, HTMX, and Tailwind CSS. The UI should be inspired by the underlying product design qualities of 37signals, specifically a hybrid of Basecamp and Fizzy. Do not copy trademarks, logos, or exact screens. Recreate the qualities instead: calm structure, strong readability, low interface noise, human product copy, layered interactions, pill and soft-rounded controls, restrained but expressive color, semantic design tokens, subtle borders, and light-but-confident surfaces.

Hard requirements:
- use Tailwind CSS
- support light and dark themes from the start
- provide two app shell variants:
  1. top navigation shell
  2. left sidebar with top utility bar shell
- provide two resource/index variants:
  1. cards/stacked-list first
  2. soft-table first
- build a reusable starter kit rather than one domain-specific module
- use Django templates first
- use HTMX for partial updates
- keep JavaScript minimal
- create reusable partials/components for buttons, forms, panels, cards, chips, empty states, soft tables, popovers, and drawers
- include accessible focus states, keyboard support, and good empty/error states

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
- card-based resource index
- soft-table resource index
- detail page
- create/edit form page
- settings page
- sign-in page
- empty-state examples page
- component playground page

Deliverables:
1. Django/Tailwind starter setup
2. token-based theme system
3. two layout shells
4. two data-view variants
5. reusable partial/component library
6. sample pages
7. theme toggle with persistence
8. HTMX demo interactions
9. README explaining architecture, tokens, components, and extension rules

Implementation style:
- prefer semantic component classes over giant repetitive utility strings
- prefer server-rendered HTML with small HTMX enhancements
- prioritize clarity, calmness, and reusability
- when in doubt, choose simpler, calmer, and more readable

---

## 24. Short prompt version for repeated future use

Use this when you do not want to paste the full brief.

### Short Codex Prompt
Create a Django starter kit with Tailwind + HTMX inspired by a Basecamp/Fizzy design hybrid: calm structure, readable typography, semantic tokens, light/dark themes, pill primary buttons, soft panels, subtle borders, layered UI, two shells (topnav and sidebar), and two index modes (cards and soft-table). Avoid generic Tailwind SaaS aesthetics and avoid default admin look. Build reusable partials and starter pages, not a domain-specific product.

---

## 25. Remaining clarification questions

These are the next questions worth answering before a v1.0 implementation brief.

1. Should UI copy inside the starter be **English** or **Polish**?
2. Do you want the starter to include **authentication screens** only at a basic level, or a fuller auth flow with reset/invite/2FA placeholders?
3. Should the default density lean more toward:
   - calm/breathable
   - balanced
   - compact/operational
4. Do you want the demo data/resource to be closer to:
   - projects/tasks
   - CRM clients/contacts
   - tickets/requests
   - generic records
5. Should the starter include a **command palette** as a real working feature or only a styled placeholder?
6. Do you want charts at all, or should the starter stay mostly text/list/form-based?
7. Should the visual brand layer be completely neutral, or do you want one extra branded accent color for your own app family?
8. Should the starter include **mobile-specific nav behavior** now, or just responsive collapse patterns?

---

## 26. Final instruction to the agent

When uncertain, choose:

- calmer over louder
- clearer over cleverer
- more readable over more decorative
- fewer visible actions over more clutter
- semantic reuse over one-off styling
- layered context over disruptive navigation
- practical product rhythm over component-demo aesthetics

The starter should feel like a product someone could work in every day.
