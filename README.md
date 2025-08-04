# Django Places Autocomplete

Django demo project showcasing Google Maps Places Autocomplete and Geocoding API v4.

## Tailwind CSS

The project uses Tailwind CSS for styling. To generate the compiled stylesheet:

```bash
npm run build:css    # Build once
npm run watch:css    # Rebuild on changes
```

The compiled file is written to `django_places_autocomplete/static/css/app.css` and is included in `base.html` via `{% static %}`.

When the build warns about outdated Browserslist data, refresh the database with:

```bash
npm run browserslist:update
```

## Tests

Run Django tests with:

```bash
python manage.py test
```

