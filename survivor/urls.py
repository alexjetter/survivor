from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^season31/', include('season31.urls', namespace="season31")),
	url(r'^$', lambda r: HttpResponseRedirect('season31/')),
]
