# pylint: disable=line-too-long,import-error,fixme
"""
Django settings for tcf_core project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = int(os.environ.get('DEBUG', 0)) == 1
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = ['localhost', '.ngrok.io', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'cachalot',  # TODO: add Redis?
    'tcf_website'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tcf_core.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'tcf_core.context_processors.base',
            ],
        },
    },
]

WSGI_APPLICATION = 'tcf_core.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
# STATIC_URL = os.environ.get('STATIC_URL', default='static/')



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'tcf_db',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'tcf_django',
        'PASSWORD': 's3kr1t',
        'HOST': 'tcf_db',
    },
    'legacy': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tcf.db'),
    },
}


# python-social-auth settings.

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['virginia.edu']
# SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
# LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_USER_MODEL = 'tcf_website.User'
AUTH_USER_MODEL = 'tcf_website.User'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'tcf_core.auth_pipeline.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'tcf_core.auth_pipeline.collect_extra_info',
    'tcf_core.auth_pipeline.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Read-only access to Elastic
ES_PUBLIC_API_KEY = os.environ.get('ES_PUBLIC_API_KEY')
ES_COURSE_SEARCH_ENDPOINT = os.environ.get('ES_COURSE_SEARCH_ENDPOINT')
ES_INSTRUCTOR_SEARCH_ENDPOINT = os.environ.get('ES_INSTRUCTOR_SEARCH_ENDPOINT')

# PROD SETTINGS
if not DEBUG:

    # Heroku configuration.
    if os.environ.get("HEROKU", False):
        import django_heroku
        django_heroku.settings(locals())

    # Gather information from environment variables.

    HOSTNAME = os.environ.get('HOSTNAME')
    PUBLIC_IPV4 = os.environ.get('PUBLIC_IPV4')

    # SECURITY WARNING: App Engine's security features ensure that it is safe to
    # have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
    # app not on App Engine, make sure to set an appropriate host here.
    # See https://docs.djangoproject.com/en/1.10/ref/settings/ (from GCP
    # documentation)
    ALLOWED_HOSTS = ['*']

    if HOSTNAME:
        ALLOWED_HOSTS.append(HOSTNAME)
    if PUBLIC_IPV4:
        ALLOWED_HOSTS.append(PUBLIC_IPV4)

    # Read-write access to Elastic
    ES_COURSE_DOCUMENTS_ENDPOINT = os.environ.get('ES_COURSE_DOCUMENTS_ENDPOINT')
    ES_INSTRUCTOR_DOCUMENTS_ENDPOINT = os.environ.get('ES_INSTRUCTOR_DOCUMENTS_ENDPOINT')
    ES_PRIVATE_API_KEY = os.environ.get('ES_PRIVATE_API_KEY')

    DATABASES['default'] = {
        'NAME': os.environ.get('DB_NAME'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {'sslmode': 'require'},
    }

    print(DATABASES['default'])
