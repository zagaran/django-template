def django_settings(request):
    from django.conf import settings
    return {
        "PRODUCTION": settings.PRODUCTION,
        "DEBUG": settings.DEBUG,
    }