# syntax=docker/dockerfile:1.7
# casedock image — three stages: py-builder (uv) → css-builder (npm) → runtime
# uv in Docker: https://docs.astral.sh/uv/guides/integration/docker/

# ─── Stage 1: Python deps via uv ─────────────────────────────────────────────
FROM python:3.13-slim AS py-builder

# Copy uv binary (not a uv-derived image): guarantees the Python path in the
# venv matches between builder and runtime. Mismatch breaks the venv on copy.
COPY --from=ghcr.io/astral-sh/uv:0.11.25 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# --locked (not --frozen): casedock is a single project, not a workspace.
# --frozen skips lockfile validation and silently allows drift.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


# ─── Stage 2: Tailwind CSS build ─────────────────────────────────────────────
FROM node:22-slim AS css-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY static/ui/input.css ./static/ui/input.css
COPY templates/ ./templates/
COPY src/ ./src/
RUN npm run build:css


# ─── Stage 3: Runtime ────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

# psycopg[binary] bundles libpq — no apt packages needed.
# If you switch to source-build psycopg, install libpq5 here.
RUN groupadd --system --gid 1001 casedock \
 && useradd  --system --uid 1001 --gid casedock --create-home casedock

WORKDIR /app

COPY --from=py-builder --chown=casedock:casedock /app /app
COPY --from=css-builder --chown=casedock:casedock /app/static/ui/tailwind.css /app/static/ui/tailwind.css
COPY --chmod=0755 docker/entrypoint.sh /app/docker/entrypoint.sh

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod

USER casedock
EXPOSE 8000

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--forwarded-allow-ips", "*"]
