from django.urls import path, include
from .views import (
    FacultyApiView,
    FacultyDetailApiView
)

urlpatterns = [
    path('', FacultyApiView.as_view()),
    path('<int:faculty_id>/', FacultyDetailApiView.as_view()),
]