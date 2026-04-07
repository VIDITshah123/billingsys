@echo off
echo Setting up VIDHIM ENTERPRISES Billing System...

REM Install dependencies
echo Installing dependencies...
pip install Django==4.2.7
pip install django-crispy-forms==2.1
pip install crispy-bootstrap5==0.7
pip install reportlab==4.0.7

REM Setup database
echo Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create superuser (optional)
echo Creating superuser account...
python manage.py createsuperuser

echo Setup complete!
echo You can now run the server with: python manage.py runserver
pause
