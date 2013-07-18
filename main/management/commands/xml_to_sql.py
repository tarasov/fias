# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.management.base import BaseCommand
import time

from main.models import AddrObj
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    args = 'path_to_fias directory'

    def handle(self, path, *args, **options):
        all_field_names = AddrObj._meta.get_all_field_names()

        xml_addrobj = os.path.join(path, 'ADDROBJ.XML')

        dump = open(os.path.join(settings.PROJECT_PATH, 'dump.sql'), 'w')
        query = 'INSERT INTO `{0}` ({1}) VALUES '.format(
            AddrObj._meta.db_table,
            ', '.join(['`{0}`'.format(field) for field in all_field_names])
        )
        insert_fields = u', '.join("'{{{0}}}'".format(field) for field in all_field_names)
        start = time.time()
        insertes = []
        try:
            for i, (event, item) in enumerate(ET.iterparse(xml_addrobj), 1):
                fields = dict((attr, item.attrib.get(attr.upper())) for attr in all_field_names)

                insertes.append(u'({0})'.format(insert_fields.format(**fields)))

                if i % 10000 == 0:
                    dump.write('{0} {1};\n'.format(query, ', '.join(insertes).encode('utf-8')))
                    insertes = []
        except UnicodeEncodeError, e:
            print i
            print insert_fields.format(**fields)
            print e
        print 'Time %.5fs ..' % (time.time() - start)
        dump.close()
