import os

from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS = (
    'modeltranslation',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mptt',
    'linaro_django_pagination',
    'webstack_django_sorting',
    'rest_framework',
    'froala_editor',
    'haystack',
    'sorl.thumbnail',
    'adminsortable2',
    'njango',
    'solo',

    'users',
    'inventory',
    'account',
    'core',
    'ils',
    'training',
    'key',
    'project',
    'authority_handover',
    'hr',
    'import_export',
    'debug_toolbar'
)

TIME_ZONE = 'Asia/Kathmandu'
DEFAULT_CALENDAR = 'bs'
USE_TZ = True
USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = 'en'
gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('ne', gettext('Nepali')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

try:
    from .local_settings import *  # noqa
except ImportError:
    pass

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/user/login/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'linaro_django_pagination.middleware.PaginationMiddleware',
    'webstack_django_sorting.middleware.SortingMiddleware',
    'njango.middleware.CalendarMiddleware',
    'key.middleware.KeyMiddleware',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.'
                  'ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

FROALA_INCLUDE_JQUERY = False

WEBPACK_ASSET_JSON = os.path.join(BASE_DIR, 'assets.json')