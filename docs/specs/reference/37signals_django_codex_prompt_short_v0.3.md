# Codex CLI Prompt — 37signals Django Starter
Version: v0.3

Build a reusable Django starter kit with Django templates, HTMX, and Tailwind CSS.

Design direction:
- inspired by the product qualities of **Basecamp + Fizzy**
- do not copy logos, trademarks, or exact screens
- recreate the feeling instead: calm structure, readable typography, low interface noise, human copy, layered interactions, soft rounded surfaces, pill primary buttons, restrained expressive color, neutral branding

Hard requirements:
- English UI copy
- light + dark theme
- calm density by default + compact density option
- two layout shells:
  - top navigation
  - left sidebar + top utility bar
- two ticket index modes:
  - cards / stacked list
  - soft table
- ticket records as the sample domain
- real working command palette (`cmd/ctrl+k`)
- auth placeholders for reset password, invite flow, and 2FA
- reusable partials/components
- HTMX for partial updates
- minimal JavaScript
- accessibility-conscious keyboard and focus behavior

Visual rules:
- mostly neutral surfaces
- blue primary accent
- occasional purple/pink/gold support accents
- subtle borders
- soft shadows only for floating layers
- calm page composition
- avoid generic Tailwind SaaS look
- avoid default admin look

Starter pages:
- dashboard
- card-based ticket index
- soft-table ticket index
- ticket detail
- create/edit form
- settings
- sign-in
- reset password placeholder
- invite placeholder
- 2FA placeholder
- empty states page
- component playground

Implementation style:
- semantic component classes over utility soup
- server-rendered HTML first
- HTMX enhancements second
- prioritize reusability, clarity, calmness, and all-day usability
