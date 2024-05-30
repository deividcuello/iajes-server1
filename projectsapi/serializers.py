from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "image_url", "slug", "college", "published_date", "start_year", "end_year", "isWorking", "industry", "investigator", "region",  "summary", "email", "approved", "keywords", "partner_organization", "user", "hidden", "created_at"]

        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class VisibleProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "image_url", "slug", "college", "published_date", "start_year", "end_year", "isWorking", "industry", "investigator", "region",  "summary", "email", "approved", "keywords", "partner_organization", "user", "hidden", "created_at"]
