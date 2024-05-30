from django.urls import path, include
from .views import (
    CenterApiView,
    CenterDetailApiView
)

urlpatterns = [
    path('', CenterApiView.as_view()),
    path('<int:center_id>/', CenterDetailApiView.as_view()),
]