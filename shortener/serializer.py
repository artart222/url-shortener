from rest_framework import serializers
from .models import Shortener


class ShortenerURLCreateRequest(serializers.ModelSerializer):
    class Meta:
        model = Shortener
        fields = ["original_url", "id"]


class ShortURLDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shortener
        fields = "__all__"
