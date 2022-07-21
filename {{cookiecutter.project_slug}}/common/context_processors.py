def django_settings(request):
    from django.config import settings
    return {
        "PRODUCTION": settings.PRODUCTION
    }