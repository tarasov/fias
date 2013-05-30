#coding: utf-8
import json
import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from kladr.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        PROJECT_ROOT = getattr(settings, 'PROJECT_PATH')
        raw = open(os.path.join('/var/www/kladr/kladr.sql'))

        print 'start'
        print 'delete objects..'
        Kladr.objects.all().delete()

        parents = {}
        print 'in iterations..'
        for raw_line in raw:
            z = zip(
                ['id', 'parent_id', 'title', 'socr', 'index', 'level', 'kladr_code', 'socr_name_id'],
                re.split('\t+', raw_line)
            )
            kw = dict(z)

            parent_id = kw['parent_id']

            if not parent_id or parent_id == '\N':
                print kw
                kladr = Kladr(**kw)
                kladr.save()
            else:
                kladr_id = kw['id']

                if parent_id in parents:
                    parents[parent_id].append(kladr_id)
                else:
                    parents[parent_id] = [kladr_id]

        print 'update objects..'
        for parent_id, kladrs in parents.iteritems():
            parent = Kladr.objects.get(id=parent_id)
            Kladr.objects.filter(id__in=kladrs).update(parent=parent)



    # def handle(self, *args, **options):
    #     PROJECT_ROOT = getattr(settings, 'PROJECT_PATH')
    #     raw = open(os.path.join(PROJECT_ROOT, 'kladr/sql/street.sql'))
    #
    #     # Street.objects.all().delete()
    #
    #     bag = []
    #
    #     for i, raw_line in enumerate(raw):
    #         id, parent_id, title, socr, index, kladr_code, socr_name_id = re.split('\t+', raw_line)
    #
    #         socr_name = None
    #         if socr_name_id.strip() != '\N':
    #             socr_name = Socr.objects.get(pk=socr_name_id.strip())
    #
    #         a = GeoIpRanges(
    #             id=id,
    #             title=title,
    #             socr=socr,
    #             index=index,
    #             klad_code=kladr_code,
    #             socr_name=socr_name,
    #         )
    #
    #         bag.append(a)
    #
    #     GeoIpRanges.objects.bulk_create(bag)

    # def handle(self, *args, **options):
    #     PROJECT_ROOT = getattr(settings, 'PROJECT_PATH')
    #     raw = open(os.path.join(PROJECT_ROOT, 'kladr/sql/house.sql'))
    #
    #     houses = []
    #     for i, raw_line in enumerate(raw):
    #         id, parent_id, title, korp, socr, index, kladr_code, parent_kladr_id = re.split('\t+', raw_line)
    #
    #         parent = None
    #         if parent_id != '\N':
    #             parent = Street.objects.get(pk=parent_id)
    #
    #         parent_kladr = None
    #         if parent_kladr_id.strip() != '\N':
    #             parent_kladr = Kladr.objects.get(pk=parent_kladr_id.strip())
    #
    #         house = House(
    #             id=id,
    #             title=title,
    #             korp=korp,
    #             socr=socr,
    #             index=index,
    #             klad_code=kladr_code,
    #             parent=parent,
    #             parent_kladr=parent_kladr,
    #         )
    #
    #         houses.append(house)
    #
    #         if i % 50000 == 0:
    #             print i
    #             try:
    #                 House.objects.bulk_create(houses)
    #             except IntegrityError:
    #                 pass
    #             houses = []
    #
    #     if houses:
    #         print '-' * 40
    #         print len(houses)
    #         print '-' * 40
    #         House.objects.bulk_create(houses)

    # def handle(self, *args, **options):
    #     PROJECT_ROOT = getattr(settings, 'PROJECT_PATH')
    #     raw = open(os.path.join(PROJECT_ROOT, 'kladr/sql/socr.sql'))
    #
    #     Socr.objects.all().delete()
    #
    #     for raw_line in raw:
    #         id, socr, title, level = re.split('\t+', raw_line)
    #
    #         Socr(
    #             id=id,
    #             socr=socr.strip(),
    #             title=title.strip(),
    #             level=level.strip()
    #         ).save()
