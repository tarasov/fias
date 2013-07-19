from django.conf.urls import patterns, include, url
from .api.resources import AddrResource


urlpatterns = patterns('',
                       url('^api/', include(AddrResource().urls)),
                       )
