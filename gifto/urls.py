from django.contrib import admin
from django.urls import path, include

from gifto.views import Home, RandomFeedbackSurvey


urlpatterns = [
	path('admin/', admin.site.urls),
	path('rest/', include('gifto.rest.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('random', RandomFeedbackSurvey.as_view(), name="random-feedback"),

	path('home', Home.as_view(), name="home")
]