from django.urls import path
from .views import *

urlpatterns = [
    path('sentiment/', AnalyzeSentiment.as_view(), name="sentiment")
]
