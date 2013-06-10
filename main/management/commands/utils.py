# coding: utf8

import os
import xml.sax
from django.db import transaction


def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n'.format(os.path.basename(xml_path))

    class FiasHandler(xml.sax.ContentHandler):
        count = 0

        @transaction.commit_manually
        def startElement(self, name, attrs):

            model.objects.all().delete()
            names = attrs.getNames()
            if names:
                self.count += 1
                data = dict((field, attrs._attrs.get(field.upper())) for field in fields)

                model(**data).save()

                if self.count % 2000 == 0:
                    transaction.commit()
                    print u'commit - {0}'.format(self.count)

    xml.sax.parse(xml_path, FiasHandler())
    transaction.commit()
    print u"### end commit"
