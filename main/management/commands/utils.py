# coding: utf8

import os
import xml.sax


def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n{1}\n'.format(os.path.basename(xml_path), xml_path)

    class FiasHandler(xml.sax.ContentHandler):
        bulk_list = []

        def startElement(self, name, attrs):
            model.objects.all().delete()
            names = attrs.getNames()
            if names:
                obj = model(dict((field, attrs._attrs.get(field.upper())) for field in fields))
                self.bulk_list.append(obj)
                if len(self.bulk_list) % 2500 == 0:
                    print u'commit - {0}'.format(self.counter)
                    model.objects.bulk_create(self.bulk_list)
                    self.bulk_list = []

            xml.sax.parse(self.xml_path, FiasHandler())
            model.objects.bulk_create(self.bulk_list)
            print u"### end commit"
