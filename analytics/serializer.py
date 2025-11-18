from rest_framework import serializers
from .models import Analytics


class AnalyticsListViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = "__all__"
