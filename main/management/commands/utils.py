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
        self.count = 0

        t1 = threading.Thread(target=self.heap)
        t1.daemon = True
        t1.start()

        t2 = threading.Thread(target=self.heap)
        t2.daemon = True
        t2.start()

        t3 = threading.Thread(target=self.heap)
        t3.daemon = True
        t3.start()

    def parse(self, fields):
        context = ET.iterparse(self.xml_path, events=('start', 'end'))
        context = iter(context)
        event, root = context.next()

        for event, elem in context:
            if event == 'start':
                self.count += 1
                data = dict((field, elem.attrib.get(field.upper())) for field in fields)
                self.addresses.append(self.model(**data))
                if self.count % 5000 == 0:
                    self.add_task((self.count, self.addresses))
                    self.addresses = []

    def heap(self):
        time.sleep(5)
        while True:
            if self.h:
                count, addresses = self.pop_task()
                self.model.objects.bulk_create(addresses)
                print 'save - {0}'.format(count)
            else:
                self.is_stop = False

            time.sleep(2)

    def pop_task(self):
        if self.h:
            count, addresses = heapq.heappop(self.h)
            del self.entry_finder[count]
            return count, addresses
        else:
            self.is_stop = False


    def add_task(self, task):
        self.entry_finder[task[0]] = task
        heapq.heappush(self.h, task)



