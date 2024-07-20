#!/usr/bin/env bash
# exit on error

set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

if [ $(python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).count())") -eq 0 ]; then
    python manage.py createsuperuser --noinput --username admin --email admin@example.com
fi