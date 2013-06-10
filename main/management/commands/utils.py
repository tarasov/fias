# coding: utf8

import os
import xml.sax


def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n{1}\n'.format(os.path.basename(xml_path), xml_path)
    bulk_list = []

    class FiasHandler(xml.sax.ContentHandler):

        def startElement(self, name, attrs):
            global bulk_list

            model.objects.all().delete()
            names = attrs.getNames()
            if names:
                obj = model(dict((field, attrs._attrs.get(field.upper())) for field in fields))
                bulk_list.append(obj)
                if len(bulk_list) % 2500 == 0:
                    print u'commit - {0}'.format(len(bulk_list))
                    model.objects.bulk_create(bulk_list)
                    bulk_list = []

    xml.sax.parse(xml_path, FiasHandler())
    model.objects.bulk_create(bulk_list)
    print u"### end commit"
