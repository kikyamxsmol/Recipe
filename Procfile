release: python manage.py migrate --noinput ; python manage.py collectstatic --noinput ; echo "Release phase complete"
web: python init_db.py && gunicorn config.wsgi
