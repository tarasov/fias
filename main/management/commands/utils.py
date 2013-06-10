# coding: utf8

import os
import xml.sax


bulk_list = []


def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n'.format(os.path.basename(xml_path))

    class FiasHandler(xml.sax.ContentHandler):
        aoids = []
        summa = 0

        def startElement(self, name, attrs):
            global bulk_list

            model.objects.all().delete()
            names = attrs.getNames()
            if names:
                data = dict((field, attrs._attrs.get(field.upper())) for field in fields)

                obj = model(**data)

                bulk_list.append(obj)
                if len(bulk_list) % 2000 == 0:
                    self.summa += len(bulk_list)
                    model.objects.bulk_create(bulk_list)
                    print u'commit - {0}'.format(self.summa)
                    bulk_list = []

                self.aoids.append(data['aoid'])

    xml.sax.parse(xml_path, FiasHandler())
    model.objects.bulk_create(bulk_list)
    print u"### end commit"
