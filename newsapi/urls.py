from django.urls import path, include
from .views import (
    NewsApiView,
    NewsDetailApiView
)

urlpatterns = [
    path('', NewsApiView.as_view()),
    path('<slug:slug>/', NewsDetailApiView.as_view()),
]