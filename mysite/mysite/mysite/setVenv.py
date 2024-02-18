def setVenv(value):
    from os import environ
    environ.setdefault("DJANGO_SETTINGS_MODULE", value)
    print(environ)
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    return application