# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand

from main.management.commands.utils import parse_fias
from main.models import AddrObj


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
                      'aolevel', 'livestatus', 'okato', 'startdate', 'updatedate', 'enddate', 'actstatus',
                      'operstatus', 'currstatus']
            parse_fias(AddrObj, fields, xml_addrobj)

