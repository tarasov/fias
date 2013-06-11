# coding: utf8

import os
import xml.sax
from django.db import connection

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

                if self.count % 3500 == 0:
                    model.objects.bulk_create(addresses)
                    print u'commit - {0}'.format(self.count)
                    addresses = []

    print u"### deleting data.."
    model.objects.all().delete()
    print u"### deleted."
    cursor = connection.cursor()
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    cursor.execute('SET UNIQUE_CHECKS = 0;')
    cursor.execute('SET AUTOCOMMIT = 0;')

    print u"### inserting data.."
    xml.sax.parse(xml_path, FiasHandler())

    model.objects.bulk_create(addresses)
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
    cursor.execute('SET UNIQUE_CHECKS = 1;')
    cursor.execute('COMMIT;')
    print u"### insert."
