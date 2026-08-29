# Casedock brand assets — Django package

Paczka zawiera gotowe pliki do użycia w aplikacji Django: SVG, PNG, favicony, ikony PWA, plik CSS z tokenami oraz mini księgę znaku.

## Szybkie użycie w Django

1. Skopiuj katalog `django_static/casedock/` do katalogu statycznego aplikacji, np.:

```bash
mkdir -p your_app/static/casedock
cp -R django_static/casedock/* your_app/static/casedock/
```

2. W szablonie dodaj:

```django
{% load static %}
<link rel="icon" href="{% static 'casedock/favicon.ico' %}">
<link rel="apple-touch-icon" href="{% static 'casedock/favicon-180x180.png' %}">
<link rel="manifest" href="{% static 'casedock/site.webmanifest' %}">
<link rel="stylesheet" href="{% static 'casedock/casedock-brand.css' %}">
```

3. Logo w jasnym trybie:

```django
<img class="casedock-logo" src="{% static 'casedock/casedock-logo-horizontal-light.svg' %}" alt="Casedock">
```

4. Logo w ciemnym trybie:

```django
<img class="casedock-logo" src="{% static 'casedock/casedock-logo-horizontal-dark.svg' %}" alt="Casedock">
```

## Rekomendowane pliki

- Header/nav: `casedock-logo-horizontal-light.svg` / `casedock-logo-horizontal-dark.svg`
- Sidebar/app launcher: `casedock-app-icon-light.svg` / `casedock-app-icon-dark.svg`
- Favicon: `favicon.ico` albo `favicon-32x32.png`
- PWA: `favicon-192x192.png`, `favicon-512x512.png`, `site.webmanifest`

## Kolory

- Ink Navy: `#0F172A`
- Muted Blue: `#8FA1B3`
- Warm White: `#FAF8F5`
- Dark Navy: `#061827`
- Dark Panel: `#0B2234`

## Uwaga projektowa

SVG są wektorowe i powinny być preferowane w UI. PNG są dodane jako fallback, do social preview, dokumentacji lub miejsc, które nie przyjmują SVG.
