"""
Django 1.11.5.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'key-key-key-key'

SITE_ID = 1
DEBUG = True
ALLOWED_HOSTS = ['*']

QUESTIONS_PER_PAGE = 5
TAGS_PER_PAGE = 12
USERS_PER_PAGE = 12
COMMENTS_MAX_SHOW = 3

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
FILE_UPLOAD_MAX_MEMORY_SIZE = 35000000

# Add reversion models to admin interface:
ADD_REVERSION_ADMIN = True

# No Recaptha SITE_KEY and SECRET KEY
NORECAPTCHA_SITE_KEY = "key-key-key-key"
NORECAPTCHA_SECRET_KEY = "key-key-key-key"

PRIVILEGES = (
    ('as_developers', 'Developers'),
    ('as_administrators', 'Developers'),
    ('as_moderators', 'Moderators'),
    ('as_members', 'Members'),
    ('as_public', 'Public')
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sitemaps',
    'django.contrib.sites',

    # 3d party apps
    'updown',
    'badges',
    'reversion',  # https://github.com/etianen/django-reversion
    'reversion_compare',  # https://github.com/jedie/django-reversion-compare
    'djipsum',  # development only

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.linkedin',

    # major aps
    'app_faq',
    'app_user',
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Auth and allauth settings
# ACCOUNT_SIGNUP_FORM_CLASS = 'app_user.forms.SignUpForm'
ACCOUNT_FORMS = {
    'signup': 'app_user.forms.SignUpForm',
    'login': 'app_user.forms.LoginForm',
    'reset_password': 'app_user.forms.ResetPasswordForm'
}
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user:email', ]
    },
    'linkedin': {
        'SCOPE': ['r_emailaddress'],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url'
        ]
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangofaq.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangofaq.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# when you want to run command: `collectstatic`, you should do this:
# comment: `STATICFILES_DIRS` and un-comment `STATIC_ROOT`
# after it, un-comment `STATICFILES_DIRS` and comment `STATIC_ROOT`
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    '/path/to/env/djangofaq/static',
)

STATIC_URL = '/static/'
#STATIC_ROOT = '/path/to/env/djangofaq/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/path/to/env/djangofaq/media'
