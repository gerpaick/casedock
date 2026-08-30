# Casedock brand assets — Django package

This package contains ready-to-use assets for a Django application: SVG and PNG files,
favicons, PWA icons, a CSS token file, and concise brand guidelines.

## Quick setup in Django

1. Copy the `django_static/casedock/` directory into the application's static directory, for
   example:

```bash
mkdir -p your_app/static/casedock
cp -R django_static/casedock/* your_app/static/casedock/
```

2. Add the following to the template:

```django
{% load static %}
<link rel="icon" href="{% static 'casedock/favicon.ico' %}">
<link rel="apple-touch-icon" href="{% static 'casedock/favicon-180x180.png' %}">
<link rel="manifest" href="{% static 'casedock/site.webmanifest' %}">
<link rel="stylesheet" href="{% static 'casedock/casedock-brand.css' %}">
```

3. Logo in light mode:

```django
<img class="casedock-logo" src="{% static 'casedock/casedock-logo-horizontal-light.svg' %}" alt="Casedock">
```

4. Logo in dark mode:

```django
<img class="casedock-logo" src="{% static 'casedock/casedock-logo-horizontal-dark.svg' %}" alt="Casedock">
```

## Recommended files

- Header/navigation: `casedock-logo-horizontal-light.svg` / `casedock-logo-horizontal-dark.svg`
- Sidebar/app launcher: `casedock-app-icon-light.svg` / `casedock-app-icon-dark.svg`
- Favicon: `favicon.ico` or `favicon-32x32.png`
- PWA: `favicon-192x192.png`, `favicon-512x512.png`, `site.webmanifest`

## Colors

- Ink Navy: `#0F172A`
- Muted Blue: `#8FA1B3`
- Warm White: `#FAF8F5`
- Dark Navy: `#061827`
- Dark Panel: `#0B2234`

## Design note

SVG files are vector-based and should be preferred in the UI. PNG files are provided as a
fallback and for social previews, documentation, or environments that do not accept SVG.
