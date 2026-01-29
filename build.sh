#!/bin/bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating categories..."
python manage.py create_categories

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete"
