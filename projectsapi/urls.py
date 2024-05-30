from django.urls import path, include
from .views import (
    ProjectsApiView,
    ProjectDetailApiView,
)

urlpatterns = [
    path('', ProjectsApiView.as_view()),
    path('<slug:slug>/', ProjectDetailApiView.as_view()),
]