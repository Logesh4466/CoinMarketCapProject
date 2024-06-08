from django.db import models
import uuid

class ScrapeJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ScrapeResult(models.Model):
    job = models.ForeignKey(ScrapeJob, on_delete=models.CASCADE, related_name='results')
    coin = models.CharField(max_length=100)
    data = models.JSONField()  
    created_at = models.DateTimeField(auto_now_add=True)
    contracts = models.JSONField(null=True, blank=True)
    official_links = models.JSONField(null=True, blank=True)
    socials = models.JSONField(null=True, blank=True)
