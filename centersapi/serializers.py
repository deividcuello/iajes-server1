from rest_framework import serializers
from .models import Center

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ["id", "cover_url", "program_name", "phone", "center", "email", "location", "hidden", "created_at"]