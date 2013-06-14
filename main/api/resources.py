from tastypie.resources import ModelResource
from main.models import AddrObj, House
from tastypie.constants import ALL


class AddrResource(ModelResource):
    class Meta:
        queryset = AddrObj.objects.filter(livestatus=True)
        allowed_methods = ['get', ]
        filtering = {
            u'formalname': ALL,
            u'aolevel': [u'exact', u'in'],
            u'parentguid': [u'exact'],
            u'aoguid': [u'exact'],
            u'centstatus': [u'exact'],
            u'postalcode': [u'exact'],
        }
        resource_name = u'addresses'


class HouseResource(ModelResource):
    class Meta:
        queryset = House.objects.all()
        allowed_methods = ['get', ]
        filtering = {
            u'formalname': ALL,
            u'aolevel': [u'exact'],
            u'aoguid': [u'exact'],
            u'postalcode': [u'exact'],
        }
        resource_name = u'houses'

