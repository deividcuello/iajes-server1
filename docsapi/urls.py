from django.urls import path, include
from .views import (
    DocApiView,
    DocDetailApiView
)

urlpatterns = [
    path('', DocApiView.as_view()),
    path('<int:doc_id>/', DocDetailApiView.as_view()),
]