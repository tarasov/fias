from django.conf.urls import include, patterns, url

from .api.resources import AddrResource


urlpatterns = patterns(
    '',
    url('^api/', include(AddrResource().urls)),
)
