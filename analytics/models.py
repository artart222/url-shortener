from django.db import models
from shortener.models import Shortener


class Analytics(models.Model):
    shortener_id = models.ForeignKey(Shortener, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    base62_code = models.CharField(max_length=10, null=True, blank=True)
    # TODO: Add these.
    # device_type
    # campaign
    # refferer
