import os
import mimetypes

mimetypes.add_type("text/css", ".css", True)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4blyti@u4yj$skr7e&g63f*l%#jl(xq&od-2y&qzo^rrs!_p#7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'accounts',
    'blogging',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',
    'label_tag_attr',
    'social_django',
    'taggit',
    'contactus',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lsupchile.middleware.LoginRequiredMiddleware',
    # 'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'lsupchile.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',  # <--
            ],

        },
    },
]

WSGI_APPLICATION = 'lsupchile.wsgi.application'


"""

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
'default': {
        'ENGINE': 'django.db.backends.mysql',  # MySql
        'NAME': 'DjangoCui',  # use create Database w3devDjangoT1 in sql terminal
        'USER': 'root',      # create a new user via root login of your workbench
        'PASSWORD': 'leanstartupchile',
        # 'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
"""


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'odoo',
        'PASSWORD': False,
        'HOTS': 'localhost',
        'PORT': 5432,
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'lsupchile/media')

LOGIN_REDIRECT_URL = '/account/home/'

LOGIN_URL = '/account/login/'

LOGIN_EXEMPT_URLS = (
    r'^$',
    r'^account/login/$',
    r'^account/home/$',
    r'^account/logout/$',
    r'^account/logout/login/$',
    r'^account/register/$',
    r'^oauth/$',
    r'^account/feed/(?P<pk>\d+)/$',
    r'^blogging/$',
    r'^account/contactus/$',
    r'^admin/$',
    r'^blogging/category/(?P<pk>\d+)/$',
    r'^blogging/(?P<pk>\d+)/$',
    r'^account/contactus/$',
    r'^account/reset-password/$',
    r'^account/reset-password/done/$',
    r'^account/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^account/reset-password/complete/$',
    r'^contact/$',
    r'^contact/success$'
)

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# For Social Auth Login
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_LOGIN_REDIRECT_URL ='/account/home/'



SOCIAL_AUTH_FACEBOOK_KEY = '839939956196894'
SOCIAL_AUTH_FACEBOOK_SECRET = '6cb02190be8c968a4099b29e75ab9c9d'


CONTACT_US_EMAIL = ['chengri1105@gmail.com',]