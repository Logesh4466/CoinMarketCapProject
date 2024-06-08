from rest_framework import serializers
from .models import ScrapeJob, ScrapeResult

class ScrapeJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeJob
        fields = ['id', 'created_at']

class ScrapeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeResult
        fields = ['coin', 'data', 'created_at', 'contracts', 'official_links', 'socials']
