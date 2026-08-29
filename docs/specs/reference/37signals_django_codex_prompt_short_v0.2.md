# Short Codex Prompt — 37signals-Inspired Django Starter

Create a reusable Django starter kit using Django templates, HTMX, and Tailwind CSS.

The UI should be inspired by a **Basecamp + Fizzy** hybrid from 37signals.
Do **not** copy exact screens, trademarks, or brand assets.
Instead reproduce the underlying qualities:

- calm structure
- strong readability
- low interface noise
- human product copy
- subtle but expressive color
- pill primary buttons
- softly rounded panels and cards
- light/dark theme support
- layered UI such as drawers, popovers, and partial page updates

Hard requirements:

- Tailwind CSS
- Django templates first
- HTMX for partial updates
- minimal JavaScript
- semantic design tokens with CSS variables
- light + dark themes
- two shell variants:
  1. top navigation shell
  2. left sidebar + top utility bar shell
- two resource/index variants:
  1. cards / stacked-list first
  2. soft-table first
- reusable starter kit, not domain-specific implementation

Visual requirements:

- mostly neutral surfaces
- blue primary action/link color
- occasional purple/pink/gold supporting accents
- dark ink text in light mode
- strong readable text in dark mode
- subtle borders
- soft shadows only for floating layers
- calm editorial page composition
- avoid generic Tailwind SaaS look
- avoid default Django admin feel

Generate:

1. base Django/Tailwind setup
2. tokenized theme system
3. two layout shells
4. reusable partials/components
5. starter pages: dashboard, card index, soft-table index, detail, form, settings, sign-in
6. theme toggle with persistence
7. HTMX demo interactions
8. README explaining architecture and extension rules

Implementation style:

- prefer semantic component classes over giant utility strings
- prefer server-rendered HTML with small HTMX enhancements
- prioritize calmness, clarity, and reusability
- when in doubt, choose simpler and more readable
