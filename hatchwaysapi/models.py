from django.db import models
from django.utils import timezone
# Create your models here.

class videoMetadata(models.Model):
    videoId = models.CharField(primary_key=True,max_length=100, blank=True, null=False)
    publishedAt = models.CharField(max_length=100, blank=True, null=True, default='')
    title = models.CharField(max_length=1000, blank=True, null=True)
    thumbnailUrl = models.CharField(max_length=1000,blank=True,null=True)
    description = models.CharField(max_length=10000,blank=True,null=True)