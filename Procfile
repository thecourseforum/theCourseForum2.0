release: python manage.py collectstatic --noinput --clear && python manage.py makemigrations && cat * && python manage.py migrate
web: gunicorn tcf_core.wsgi --log-level debug
