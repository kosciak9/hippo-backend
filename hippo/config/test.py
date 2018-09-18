import os

from hippo.config.common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Test(Common):
    DEBUG = True
    SECRET_KEY = os.getenv(
        'DJANGO_SECRET_KEY',
        default='d&u^gojt76iv-9a&)uthyumu1*htjn)5_7vp%i@#^5e%-3*@io'
    )

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    '''
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package=hippo',
        '--cover-html'
    ]
    '''

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
