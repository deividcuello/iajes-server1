from django.urls import path, include
from .views import (
    RegionalAssociationApiView,
    RegionalAssociationDetailApiView
)

urlpatterns = [
    path('', RegionalAssociationApiView.as_view()),
    path('<int:video_id>/', RegionalAssociationDetailApiView.as_view()),
]