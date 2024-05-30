from rest_framework import serializers
from .models import RegionalAssociation

class RegionalAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionalAssociation
        fields = ["id", "video_url", "title",  "region","hidden", "created_at"]