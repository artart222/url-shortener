from django.db import models


# Create your models here.
class Shortener(models.Model):
    original_url = models.URLField()
    shortened_url = models.URLField(null=True, blank=True)
    base62_code = models.CharField(max_length=10, null=True, blank=True)
    # TODO: Maybe add created by in future.
    # TODO: Maybe add created at in future.
