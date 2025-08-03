############################
# 1️⃣ Node stage – Tailwind
############################
FROM node:20-bullseye-slim AS frontend

WORKDIR /src

# Copy package.json and package-lock.json for better cache
COPY package*.json ./
COPY postcss.config.js ./
COPY tailwind.config.js ./

RUN npm install

# Copy only what's needed to build CSS (faster cache)
COPY assets/ ./assets/

# Build the Tailwind CSS file
RUN npx tailwindcss -i ./assets/css/input.css -o /app.css --minify

############################
# 2️⃣ Python stage – Django
############################
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bring the compiled stylesheet into Django's static files
COPY --from=frontend /app.css ./static/css/app.css

# Copy everything else (Django app code, etc.)
COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "django_places_autocomplete.myproject.wsgi:application", "-b", "0.0.0.0:8000"]

