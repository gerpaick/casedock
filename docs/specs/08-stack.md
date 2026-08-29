# Recommended Stack

## Goal of the stack

The stack should support a product that is:
- calm
- text-first
- workflow-heavy
- single-user first, with room for later multi-user support
- easy to iterate on
- ready for source integrations later, with ClickUp first

This is not a front-end platform product.
It is a **workbench for decisions, execution, and reduced cognitive friction**.

Because of that, the stack should optimize for:
- fast iteration
- strong domain modeling
- low cognitive overhead
- server-rendered speed and simplicity
- text and workflow over rich front-end complexity

## Recommended stack

### Backend
- **Django 6.0**
- **Django Ninja** for selective API endpoints

### Frontend
- **Django templates**
- **HTMX**
- **Alpine.js**
- **Tailwind CSS**

### Data and infrastructure
- **PostgreSQL**
- **Redis**
- **Celery**

### Deployment
- **Docker Compose**
- **Caddy** as reverse proxy

### Optional later
- **Meilisearch** for richer search
- **S3-compatible object storage** for attachments/artifacts

## Why this stack fits the product

### 1. Django is a better fit than a custom API-first backend
The product has strong workflow and state needs:
- Inbox Items
- Cases
- Decisions
- Execution records
- Focus
- source links
- private notes

This is classic domain-heavy application work.
Django gives a strong foundation for:
- relational models
- migrations
- auth
- sessions
- admin
- permissions later
- server-side rendering

It is also fast to shape and evolve.

### 2. Server-rendered UI matches the product philosophy
This product should feel:
- calm
- immediate
- text-first
- low-noise

A heavy SPA would likely add too much technical and mental overhead.
With Django templates + HTMX, the product can still feel modern while staying simple.

This supports:
- inline state changes
- partial page updates
- side panels
- fast board interactions
- modal conversion flows
- low-JS architecture

### 3. Alpine.js is enough for local interactivity
Small interface behaviors such as:
- dropdowns
- local toggles
- command menu interactions
- compact vs calm mode switches
- small inline UI state

can be handled cleanly by Alpine without introducing a larger front-end framework.

### 4. Tailwind is the right UI foundation
The product will likely need:
- a highly intentional visual system
- strong spacing rules
- calm typography
- board/card layouts
- excellent dark mode
- quick experimentation with variants

Tailwind is well aligned with this design process.

### 5. PostgreSQL is the right primary store
The product is relational by nature.
Core relationships include:
- Inbox Item -> Case
- Case -> Decisions
- Case -> Execution Items
- Case -> Source Links
- Case -> Focus state
- Case -> Notes

PostgreSQL is a safe and powerful default for this.

### 6. Redis + Celery prepares the product for integrations
Even if MVP stays mostly local and simple, background jobs will matter soon for:
- source import/sync
- webhook processing
- AI transformations
- email sending
- indexing
- digest generation
- sync retries

This is a good reason to adopt Redis + Celery early, even if initial usage is light.

## Recommended implementation style

## Monolith first
This should begin as a **modular monolith**.

Not microservices.
Not frontend/backend split as separate products.

Recommended shape:
- one Django app deployment
- one PostgreSQL database
- one Redis instance
- one Celery worker
- one reverse proxy

This keeps the system understandable and fast to build.

## API strategy
The app should be **HTML-first**.

Meaning:
- the primary UI is rendered server-side
- HTMX handles partial updates
- only some areas expose JSON APIs

Good uses for Django Ninja:
- integration endpoints
- webhook receivers
- AI helper endpoints
- future external client support

Bad use in v1:
- making the whole product depend on a full front-end API architecture

## Search strategy

### V1
Use PostgreSQL-based search only.

Recommended initial approach:
- title search
- basic content search for specs/notes
- status/type filters
- source filters

### Later
Add Meilisearch only if search becomes central to the UX.

Examples:
- command-palette-quality search
- cross-case instant search
- fast note lookup across many records

## Markdown strategy

Markdown should be first-class.

Recommended approach:
- store raw markdown in the database
- render it server-side
- allow clean export to `.md`
- allow import from markdown later if useful

Do not make filesystem storage the primary source in v1.

Why:
- more complexity around sync and file integrity
- harder multi-device consistency
- harder auth and access control later

## Auth strategy

V1 should use standard Django auth.

Recommended early model:
- email + password for dev/admin simplicity
- no username-based login in the product UI
- add magic-link flow later if desired

This product does not need a custom auth system in the beginning.
It needs stable access control with low implementation cost.

Even though v1 is single-user, avoid data modeling shortcuts that make later per-user ownership impossible.

Implementation default for bootstrap:
- start with a custom user model from the first migration
- use unique email as the login identifier
- do not expose username fields or username-based flows in the product UI
- keep the auth model compatible with later multi-user ownership, even though v1 is single-user

## Source integration fit

The stack supports the source-integration roadmap cleanly.

### Phase 1
No live integration required.
Use generic SourceLink model only.

### Phase 2
Add read-only connector sync, starting with ClickUp:
- manual connect
- assigned-to-me tasks import
- Inbox Item creation from external tasks

### Phase 3
Add webhook handling and explicit write-back:
- comments
- status updates
- sync history

Django + Celery is a very good fit for this progression.

## AI fit

The stack should support AI as a helper layer, not as the core architecture.

Good AI actions:
- summarize inbox item
- convert item to Case draft
- propose next steps
- extract decisions from notes
- draft source-system update

Suggested technical pattern:
- background or on-demand endpoint
- result stored in DB
- user explicitly accepts or discards output

This works well in Django and does not require a separate AI service initially.

## Suggested library/tooling direction

These are not mandatory, but they fit the product well.

### Python
- Python 3.13 if environment is ready
- otherwise Python 3.12

### Django support libraries
- `django-ninja` for typed APIs
- `django-environ` or similar for settings
- `psycopg` for PostgreSQL
- `markdown-it-py` or another safe markdown renderer
- `bleach` or equivalent HTML sanitization if needed
- `celery`
- `redis`

### Front-end
- Tailwind CSS
- HTMX
- Alpine.js

### Quality/tooling
- `pytest`
- `pytest-django`
- `ruff`
- `mypy` optional
- pre-commit hooks

### Local tooling conventions
- `uv` for Python environment management, dependency installation, and local command execution
- `npm` only for front-end asset tooling where needed
- keep the front-end pipeline lightweight; Tailwind should compile to a static asset without introducing a SPA build architecture

## Suggested project layout

```text
casedock/
  manage.py
  src/
    config/
      settings/
      urls.py
      asgi.py
      wsgi.py
    apps/
      core/
      inbox/
      cases/
      decisions/
      execution/
      focus/
      sources/
      clickup/
      ai/
      ui/
  templates/
  static/
  tests/
  docker/
```

This structure supports a modular monolith and leaves room for future integrations.

## Bootstrap defaults for Stage 1

### Runtime direction
- target Python runtime: 3.13
- minimum supported fallback during early development: 3.12
- framework baseline: Django 6

### Supported environments
- `local` for daily development
- `test` for automated test execution
- `prod` reserved now and implemented as a minimal settings target before deployment work starts

The first scaffold must include `local` and `test`.
`prod` does not need production infrastructure in Stage 1, but the settings module path must exist.

### Settings strategy
- keep Django settings under `src/config/settings/`
- use `base.py` for shared defaults
- use `local.py`, `test.py`, and `prod.py` for environment-specific overrides
- select the active settings module through `DJANGO_SETTINGS_MODULE`
- use environment variables for secrets, connection strings, and deployment-specific values
- keep defaults safe for local development and explicit for test and prod
- use SQLite as the default local development database for the initial scaffold
- keep PostgreSQL as the primary non-local database direction for the product

### Required environment variables for initial bootstrap
- `DJANGO_SETTINGS_MODULE`
- `SECRET_KEY`

`DATABASE_URL` is not required for the default local SQLite setup.
It becomes required for non-local PostgreSQL-backed environments.

### Environment variables that should exist early, with safe local defaults if possible
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `EMAIL_BACKEND`
- `DEFAULT_FROM_EMAIL`

### Mandatory local startup versus deferred services
Mandatory in the first working scaffold:
- Django app
- SQLite-backed local development setup
- `pytest`
- `ruff`

Allowed to be deferred until the first job-backed or integration-backed workflow lands:
- Redis process
- Celery worker and scheduler
- Docker Compose orchestration
- Caddy reverse proxy
- external email provider setup

### Naming and layout conventions
- Django apps live under `src/apps/<app_name>/`
- domain app names must match the canonical module names exactly: `inbox`, `cases`, `decisions`, `execution`, `focus`, `sources`, `clickup`, `ai`
- shared support apps may exist as `core` and `ui`, but they must not absorb domain behavior that belongs in the domain apps
- templates live under `templates/<app_name>/`
- static assets live under `static/<app_name>/`
- test modules live under `tests/`
- config code lives under `src/config/`
- keep module, package, and template names lowercase

### Testing and quality gate
Minimum expectations for new work:
- add tests for new workflow logic and state transitions
- prefer request or integration tests for core HTML-first flows
- keep unit tests focused on domain rules and conversion behavior

Minimum gate before leaving Stage 1:
- the scaffold boots with `local` settings against SQLite
- `manage.py check` passes
- `pytest` passes
- `ruff check` passes
- the initial app structure matches the documented module boundaries
- the implementation can be continued without making fresh architecture decisions

## What not to do in v1

Avoid these choices early:
- React/Next SPA as the main UI
- microservices
- event bus architecture
- separate auth service
- separate markdown service
- websocket-heavy architecture from day one
- search engine before search is truly needed
- over-modeled workflow engines

These would likely slow down learning and delivery.

## Final recommendation

The recommended stack is:

- **Django 6.0**
- **Django templates**
- **HTMX**
- **Alpine.js**
- **Tailwind CSS**
- **PostgreSQL**
- **Redis**
- **Celery**
- **Docker Compose**
- **Caddy**

This stack is highly aligned with the product:
- calm
- text-first
- decision-oriented
- fast to iterate
- realistic for solo development
- ready for source integrations later

## Engineering defaults

- work spec-driven-first from `docs/specs`
- use `pytest` for automated tests by default
- add tests with new workflow and domain logic changes
- prefer request/integration tests for core HTML-first flows
