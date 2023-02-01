from django.urls import path
from .views import *

urlpatterns = [
    path("session/", SessionTrack.as_view()),
    path("exercise/", WeightExerciseTrack.as_view()),
    path("setrep/", SetRepInfoTrack.as_view()),
]