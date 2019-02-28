
release: python manage.py makemigrations guest
release: python manage.py makemigrations employee
release: python manage.py makemigrations reservations
release: python manage.py migrate guest
release: python manage.py migrate employee
release: python manage.py migrate reservations

web: gunicorn trippinTacos.wsgi --log-file -