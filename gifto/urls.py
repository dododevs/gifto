from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from gifto.views import Home, RandomFeedbackSurvey


urlpatterns = [
	path('admin/', admin.site.urls),
	path('rest/', include('gifto.rest.urls')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('random', RandomFeedbackSurvey.as_view(), name="random-feedback"),

	path('', Home.as_view(), name="home")
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)