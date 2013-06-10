# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from main.management.commands.utils import parse_fias
from main.models import House


class Command(BaseCommand):
    args = 'path_to_fias directory'

    def handle(self, path, *args, **options):
    
        if not os.path.exists(path):
            print 'Path does not exist'
            return

        xml_list = os.listdir(path)
        xml_house = None

        for xml_file in xml_list:
            if 'HOUSE' in xml_file:
                xml_house = os.path.join(path, xml_file)

        if xml_house:
            fields = ['houseid', 'houseguid', 'aoguid', 'postalcode', 'housenum', 'eststatus', 'strstatus',
                      'buildnum', 'strucnum', 'startdate', 'updatedate', 'enddate', 'okato']

            parse_fias(House, fields, xml_house)
