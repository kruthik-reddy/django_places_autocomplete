# Django Places Autocomplete

## Setup

1. Clone the repo
2. Create and activate a virtualenv

```bash
pip install -r requirements.txt
cp .env.example .env  # set GOOGLE_MAPS_API_KEY
python manage.py migrate
python manage.py runserver
```

3. Visit http://127.0.0.1:8000/address/

### Features

- Google Places Autocomplete
- Hidden address components
- AJAX form submission
- Tailwind CSS styling
