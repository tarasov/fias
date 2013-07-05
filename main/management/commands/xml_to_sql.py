# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.management.base import BaseCommand

from main.models import AddrObj
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    args = 'path_to_fias directory'

    def handle(self, path, *args, **options):
    
        all_field_names = AddrObj._meta.get_all_field_names()

        xml_addrobj = os.path.join(path, 'ADDROBJ')

        dump = open(os.path.join(settings.PROJECT_PATH, 'dump.sql'), 'w')

        tree = ET.parse(xml_addrobj)
        root = tree.getroot()

        query = u'INSERT INTO `{0}` ({1}) \n VALUES'.format(AddrObj._meta.db_table, all_field_names)
        insert_fields = u''.join(u'{0}'.format(field) for field in all_field_names)

        for i, item in enumerate(root):

            fields = dict((attr, item.attrib.get(attr.upper())) for attr in all_field_names)

            query += insert_fields.format(**fields)

            if i % 10000 == 0:
                dump.write(u'{0}{1}\n'.format(query, insert_fields))
                insert_fields = u''
