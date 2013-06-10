# coding: utf8

import os
import xml.sax


bulk_list = []

def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n'.format(os.path.basename(xml_path))

    class FiasHandler(xml.sax.ContentHandler):

        def startElement(self, name, attrs):
            global bulk_list

            model.objects.all().delete()
            names = attrs.getNames()
            if names:
                data = dict((field, attrs._attrs.get(field.upper())) for field in fields)
                print data
                obj = model(data)
                bulk_list.append(obj)
                if len(bulk_list) % 2500 == 0:
                    model.objects.bulk_create(bulk_list)
                    print u'commit - {0}'.format(len(bulk_list))
                    bulk_list = []

    xml.sax.parse(xml_path, FiasHandler())
    model.objects.bulk_create(bulk_list)
    print u"### end commit"
