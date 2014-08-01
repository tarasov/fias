# coding: utf-8
from __future__ import unicode_literals

import datetime
import decimal

import simplejson as json

from django.http import HttpResponse
from django.views.generic import View
from django.forms.models import model_to_dict
from django.db.models import Q

from main.models import AddrObj


class AddressView(View):

    def get(self, request):
        qs_filters = {}
        for filter_expr, value in dict(request.GET).items():
            filter_bits = filter_expr.split('__')
            field_name = filter_bits.pop(0)
            field_type = 'exact'

            if field_name not in AddrObj._meta.get_all_field_names():
                continue

            if len(filter_bits):
                field_type = filter_bits.pop()

            qs_filter = '__'.join([field_name, field_type])

            if field_type != 'in':
                value = value[0]

            qs_filters[qs_filter] = value

        formalname = qs_filters.get('formalname__istartswith', '')

        queryset = AddrObj.objects.filter(
            livestatus=True, enddate__gte=datetime.date.today(),
        ).order_by('formalname', 'aolevel')
        result = []

        if 'aoguid__exact' in qs_filters:
            q_obj2 = Q(
                aoguid=qs_filters['aoguid__exact'],
                aolevel=1
            )
            q_obj = q_obj2 | Q(**qs_filters)
        else:
            q_obj2 = Q(
                formalname__in=['Москва', 'Санкт-Петербург'],
                formalname__istartswith=formalname,
                aolevel=1
            )
            q_obj = q_obj2 | Q(**qs_filters)

        addresses = queryset.filter(q_obj)
        for address in addresses[:30]:
            address = model_to_dict(address)
            result.append(address)
            while True:
                parentguid = address['parentguid']
                if parentguid == 'None':
                    break

                _address = address
                try:
                    address = model_to_dict(queryset.get(aoguid=parentguid))
                except AddrObj.DoesNotExist:
                    break
                _address['parent'] = address

        return HttpResponse(
            json.dumps(result, default=json_encode_plus),
            mimetype='application/json'
        )


def json_encode_plus(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y.%m.%d %H:%M')
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y.%m.%d')
    raise TypeError(repr(obj) + " is not JSON serializable")
