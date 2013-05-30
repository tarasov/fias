from django.conf.urls import patterns, include, url
from .api.resources import AddrResource, HouseResource

from tastypie.api import Api

api = Api()
api.register(AddrResource())
api.register(HouseResource())

urlpatterns = patterns('',
                       url('^api/', include(api.urls)),
                       )
