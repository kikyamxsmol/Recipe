release: python manage.py migrate --noinput && python manage.py create_categories && python manage.py collectstatic --noinput
web: python init_db.py && gunicorn config.wsgi
