from django.urls import path
from .views import *

urlpatterns = [
    path("process_audio/", ProcessAudioView.as_view(), name="process_audio"),
    path("hello/", Hello.as_view(), name="hello"),
    path("show/", FetchAllAudioRecordsView.as_view(), name="show")
]