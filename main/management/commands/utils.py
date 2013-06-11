# coding: utf8

import os
import xml.sax
from django.db import transaction

addresses = []


def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n'.format(os.path.basename(xml_path))

    class FiasHandler(xml.sax.ContentHandler):
        count = 0

        def startElement(self, name, attrs):
            global addresses
            names = attrs.getNames()
            if names:
                self.count += 1
                data = dict((field, attrs._attrs.get(field.upper())) for field in fields)

                addresses.append(model(**data))

                if self.count % 5000 == 0:
                    model.objects.bulk_create(addresses)
                    print u'commit - {0}'.format(self.count)
                    addresses = []

    model.objects.all().delete()
    xml.sax.parse(xml_path, FiasHandler())
    model.objects.bulk_create(addresses)
    print u"### end commit"
