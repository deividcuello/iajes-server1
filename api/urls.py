from django.urls import path, include
from rest_framework import routers
# from users.views import UserViewSet

urlpatterns = [
    path("uploadadapter/", include("uploadadapterapi.urls")),
    path("projects/", include("projectsapi.urls")),
    path("centers/", include("centersapi.urls")),
    path("news/", include("newsapi.urls")),
    path("docs/", include("docsapi.urls")),
    path("faculty/", include("facultyapi.urls")),
    path("regionalasociations/", include("regionalassociationsapi.urls")),
    path("videos/", include("videosapi.urls")),
    path("email/", include("emailapi.urls")),
    path("auth/", include("users.urls")),
    path('api-auth/', include('rest_framework.urls')),
]