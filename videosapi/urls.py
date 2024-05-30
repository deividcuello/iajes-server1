from django.urls import path, include
from .views import (
    VideoApiView,
    VideoDetailApiView
)

urlpatterns = [
    path('', VideoApiView.as_view()),
    path('<int:video_id>/', VideoDetailApiView.as_view()),
]