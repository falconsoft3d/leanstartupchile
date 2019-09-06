# leanstartupchile
Lean Startup Chile

```
virtualenv djangovenv
cd djangovenv
source bin/activate
pip install django
cd djangovenv

pip install certifi==2018.4.16
pip install chardet==3.0.4
pip install Django==1.11.13 -e git+https://github.com/c-bata/django-label-tag-attr@d23393e12870d7b246f29058a490bb2b2639bc79#egg=django_label_tag_attr
pip install django-taggit==0.22.2
pip install django-widget-tweaks==1.4.2
pip install idna==2.6
pip install MySQL-python==1.2.5
pip install oauthlib==2.0.7
pip install Pillow==5.1.0
pip install PyJWT==1.6.1
pip install python-openid==2.2.5
pip install pytz==2018.4
pip install requests==2.18.4
pip install requests-oauthlib==0.8.0
pip install six==1.11.0
pip install social-auth-app-django==2.1.0
pip install social-auth-core==1.7.0
pip install urllib3==1.22

cd leanstartupchile
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
python manage.py runserver

```


1> create DjangoCui database in your mysql.

2> create the virtualenv.
    $ virtualenv djangovenv
activate the virtualenv in the terminal
    $ source djangovenv/bin/activate
install django with this command.
    pip install django


3>$ python manage.py migrate
4>$ python manage.py createsuperuser
5>$ python manage.py runserver
5>localhost:8000
6> login by superuser.



# Database
(admin;'admin', email:'admin@admin.com', pwd:'12345qwert')
```
