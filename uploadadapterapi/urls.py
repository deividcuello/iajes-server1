from django.urls import path, include
from .views import (
    UploadAdapterApiView,
)

urlpatterns = [
    path('', UploadAdapterApiView.as_view()),
]