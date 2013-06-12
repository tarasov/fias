# coding: utf8
from heapq import heappush
import os
import threading
import xml.sax
from django.db import connection

addresses = []


def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n'.format(os.path.basename(xml_path))

    print u"### deleting data.."
    model.objects.all().delete()
    print u"### deleted."
    cursor = connection.cursor()
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    cursor.execute('SET UNIQUE_CHECKS = 0;')
    cursor.execute('SET AUTOCOMMIT = 0;')

    print u"### inserting data.."
    xml.sax.parse(xml_path, FiasHandler(fields=fields))

    model.objects.bulk_create(addresses)
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
    cursor.execute('SET UNIQUE_CHECKS = 1;')
    cursor.execute('COMMIT;')
    print u"### insert."


class FiasHandler(xml.sax.ContentHandler):
    def __init__(self, *args, **kwargs):
        self.count = 0
        self.fields = kwargs.get('fields')
        self.model = kwargs.get('model')
        self.h = []
        t1 = threading.Thread(target=self.heap)
        t1.daemon = True
        t1.start()

        super(FiasHandler, self).__init__(*args, **kwargs)

    def startElement(self, name, attrs):
        global addresses
        names = attrs.getNames()
        if names:
            self.count += 1
            data = dict((field, attrs._attrs.get(field.upper())) for field in self.fields)

            addresses.append(self.model(**data))

            if self.count % 2500 == 0:
                # self.model.objects.bulk_create(addresses)
                print u'commit - {0}'.format(self.count)
                heappush(self.h, (self.count, addresses))
                addresses = []

    def heap(self):
        pass
