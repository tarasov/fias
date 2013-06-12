# coding: utf8
import heapq
from multiprocessing import heap
import os
import threading
import xml.sax
import xml.etree.ElementTree as ET
import itertools
from django.db import connection
import time
import logging


def parse_fias(model, fields, xml_path):
    print u'Начинаем парсить {0}\n'.format(os.path.basename(xml_path))

    print u"### deleting data.."
    model.objects.all().delete()
    print u"### deleted."
    cursor = connection.cursor()
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    cursor.execute('SET UNIQUE_CHECKS = 0;')
    cursor.execute('SET AUTOCOMMIT = 0;')
    logger = logging.getLogger('')
    for handler in logger.handlers:
        logger.removeHandler(handler)

    print u"### inserting data.."
    px = ParserXml(model, xml_path)
    px.parse(fields)

    while px.is_stop:
        print px.is_stop
        time.sleep(10)

    model.objects.bulk_create(px.addresses)
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
    cursor.execute('SET UNIQUE_CHECKS = 1;')
    cursor.execute('COMMIT;')
    print u"### insert."


class ParserXml(object):
    def __init__(self, model, xml_path):
        self.xml_path = xml_path
        self.model = model
        self.h = []
        self.is_stop = True
        self.REMOVED = '<removed-task>'
        self.entry_finder = {}
        self.addresses = []

        t1 = threading.Thread(target=self.heap)
        t1.daemon = True
        t1.start()

        # t2 = threading.Thread(target=self.heap)
        # t2.daemon = True
        # t2.start()
        #
        # t3 = threading.Thread(target=self.heap)
        # t3.daemon = True
        # t3.start()

        logger = logging.getLogger('')
        for handler in logger.handlers:
            logger.removeHandler(handler)

    def parse(self, fields):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        print root.attrib
        for i, child in enumerate(root, 1):
            data = dict((field, child.attrib.get(field.upper())) for field in fields)
            self.addresses.append(self.model(**data))
            print i
            if i % 500 == 0:
                print u'commit - {0}'.format(i)
                self.add_task((i, self.addresses))
                self.addresses = []

    def heap(self):
        time.sleep(5)
        while True:
            print len(self.h)
            if self.h:
                addresses = self.pop_task()
                self.model.objects.bulk_create(addresses)
                print 'save bulk {0}'.format(len(addresses))
            else:
                self.is_stop = False

            time.sleep(3)

    def pop_task(self):
        if self.h:
            count, addresses = heapq.heappop(self.h)
            del self.entry_finder[count]
            print 'pop task {0}'.format(count)
            return addresses
        else:
            self.is_stop = False


    def add_task(self, task):
        self.entry_finder[task[0]] = task
        heapq.heappush(self.h, task)
        print 'push task {0}'.format(task[0])



