from rest_framework import serializers
from .models import UploadAdapter

class UploadAdapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadAdapter
        fields = ["id", "image", "user"]