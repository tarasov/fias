# -*- coding: utf-8 -*-
import os
import xml.sax
import MySQLdb

from django.conf import settings
from django.core.management.base import BaseCommand
from main.management.commands.utils import parse_fias

from main.models import AddrObj


db = MySQLdb.connect(
    host=settings.DATABASES['default']['HOST'],
    user=settings.DATABASES['default']['USER'],
    passwd=settings.DATABASES['default']['PASSWORD'],
    db=settings.DATABASES['default']['NAME'],
    charset='utf8'
)
cursor = db.cursor()


class Command(BaseCommand):
    args = 'path_to_fias directory'

    def handle(self, path, *args, **options):
    
        if not os.path.exists(path):
            print 'Path does not exist'
            return

        xml_list = os.listdir(path)
        xml_addrobj = None

        for xml_file in xml_list:
            if 'ADDROBJ' in xml_file:
                xml_addrobj = os.path.join(path, xml_file)

        if xml_addrobj:
            fields = ['aoid', 'aoguid', 'parentguid', 'formalname', 'postalcode', 'shortname', 'centstatus',
                      'aolevel', 'livestatus', 'okato', 'startdate', 'updatedate', 'enddate']
            parse_fias(AddrObj, fields, xml_addrobj)

