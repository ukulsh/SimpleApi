from rest_framework import serializers
from .models import *

class videoMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model=videoMetadata
        fields="__all__"