from django.contrib import admin
from django.urls import path, include

from gifto.views import RandomFeedbackSurvey


urlpatterns = [
	path('admin/', admin.site.urls),
	path('rest/', include('gifto.rest.urls')),
	path('random', RandomFeedbackSurvey.as_view(), name="random-feedback")
]