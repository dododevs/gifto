from django.urls import path, include
from gifto.rest.views import RandomFeedback

urlpatterns = [
  path('catfeedback/random', RandomFeedback.as_view(), name="rest-random-feedback")
]