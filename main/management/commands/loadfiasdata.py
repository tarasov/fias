# -*- coding: utf-8 -*-
import os
import xml.sax
import MySQLdb

from django.conf import settings
from django.core.management.base import BaseCommand

from main.models import *


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
        xml_house = None

        for xml_file in xml_list:
            if 'HOUSE' in xml_file:
                xml_house = os.path.join(path, xml_file)

        if xml_house:
            self.parse_house(xml_house)

    def parse_house(self, xml_path):
        House.objects.all().delete()

        print u'Начинаем парсить House'
        print xml_path
        print

        class EventHandler(xml.sax.ContentHandler):
            counter = 0

            def startElement(self, name, attrs):
                names = attrs.getNames()
                if names:
                    self.counter += 1
                    sql = """INSERT INTO `main_house` (
                        `houseid`,
                        `houseguid`,
                        `aoguid`,
                        `postalcode`,

                        `housenum`,
                        `eststatus`,
                        `strstatus`,
                        `buildnum`,
                        `strucnum`,

                        `startdate`,
                        `updatedate`,
                        `enddate`
                    ) VALUES (
                        '%(houseid)s',
                        '%(houseguid)s',
                        '%(aoguid)s',
                        '%(postalcode)s',

                        '%(housenum)s',
                        '%(eststatus)s',
                        '%(strstatus)s',
                        '%(buildnum)s',
                        '%(strucnum)s',

                        '%(startdate)s',
                        '%(updatedate)s',
                        '%(enddate)s'
                    )""" % {
                        'houseid': attrs.getValue('HOUSEID'),
                        'houseguid': attrs.getValue('HOUSEGUID'),
                        'aoguid': attrs._attrs.get('AOGUID'),
                        'postalcode': attrs._attrs.get('POSTALCODE'),

                        'housenum': attrs._attrs.get('HOUSENUM'),
                        'eststatus': int(attrs.getValue('ESTSTATUS')),
                        'strstatus': int(attrs.getValue('STRSTATUS')),
                        'buildnum': attrs._attrs.get('BUILDNUM'),
                        'strucnum': attrs._attrs.get('STRUCNUM'),

                        'startdate': attrs.getValue('STARTDATE'),
                        'updatedate': attrs.getValue('UPDATEDATE'),
                        'enddate': attrs.getValue('ENDDATE'),
                    }
                    cursor.execute(sql)
                    if self.counter % 2000 == 0:
                        print u'commit - {0}'.format(self.counter)
                        db.commit()

        xml.sax.parse(xml_path, EventHandler())
        db.commit()
        print u"### end commit"


