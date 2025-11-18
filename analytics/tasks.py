from celery import shared_task
from .models import Analytics


@shared_task
def save_analytics_task(shortener_id, ip, browser, os, country, short_code):
    Analytics.objects.create(
        shortener_id=shortener_id,
        ip_address=ip,
        browser=browser,
        operating_system=os,
        country=country,
        base62_code=short_code,
    )
