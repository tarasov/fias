# -*- coding: utf-8 -*-
from django.db import models

AOLEVEL_CHOICES = (
    (1, u'уровень региона'),
    (2, u'уровень автономного округа'),
    (3, u'уровень района'),
    (4, u'уровень города'),
    (5, u'уровень внутригородской территории'),
    (6, u'уровень населенного пункта'),
    (7, u'уровень улицы'),
    (90, u'уровень дополнительных территорий'),
    (91, u'уровень подчиненных дополнительным территориям объектов'),
)

ESTSTATUS_CHOICES = (
    (1, u'владение'),
    (2, u'дом'),
    (3, u'домовладение'),
    (4, u'участок'),
)

STRSTATUS_CHOICES = (
    (1, u'строение'),
    (2, u'сооружение'),
    (3, u'литер'),
)

CENTSTATUS_CHOICES = (
    (0, u'объект не является центром административно-территориального образования'),
    (1, u'объект является центром района'),
    (2, u'объект является центром (столицей) региона'),
    (3, u'объект является одновременно и центром района и центром региона'),
)


class AddrObj(models.Model):
    u"""ADDROBJ (Object) содержит коды, наименования и типы адресообразующих элементов (регионы; округа;
    районы (улусы, кужууны); города, внутригородские районы,  поселки городского типа, сельские населенные пункты;
    улицы, дополнительные адресные элементы, элементы улично-дорожной сети,
    планировочной структуры дополнительного адресного элемента).
    """
    aoid = models.CharField(max_length=36, verbose_name=u'Уникальный идентификатор записи. Ключевое поле.',
                            primary_key=True)
    aoguid = models.CharField(max_length=36, verbose_name=u'Глобальный уникальный идентификатор адресного объекта',
                              db_index=True)
    parentguid = models.CharField(max_length=36, verbose_name=u'Идентификатор объекта родительского объекта',
                                  blank=True, null=True, db_index=True)
    formalname = models.CharField(max_length=120, verbose_name=u'Формализованное наименование', db_index=True)
    postalcode = models.CharField(max_length=6, verbose_name=u'Почтовый индекс', blank=True, null=True)
    shortname = models.CharField(max_length=10, verbose_name=u'Краткое наименование типа объекта')
    okato = models.CharField(max_length=11, verbose_name=u'Код ОКАТО', blank=True, null=True)
    centstatus = models.IntegerField(choices=CENTSTATUS_CHOICES, verbose_name=u'Статус центра', blank=True, null=True)
    aolevel = models.IntegerField(choices=AOLEVEL_CHOICES, verbose_name=u'Уровень адресного объекта', db_index=True)
    startdate = models.DateField(verbose_name=u'Начало действия записи')
    updatedate = models.DateField(verbose_name=u'Дата внесения записи')
    enddate = models.DateField(verbose_name=u'Окончание действия записи')
    livestatus = models.BooleanField(verbose_name=u'Признак действующего адресного объекта')

    class Meta:
        verbose_name = u'Классификатор адресообразующих элементов'
        db_table = u'addrobj'

    def __unicode__(self):
        return u"%s %s" % (self.shortname, self.formalname)

    def get_parent(self):
        if self.parentguid:
            return list(AddrObj.objects.filter(aoguid=self.parentguid, livestatus=True))
        return []

    def get_childs(self):
        return AddrObj.objects.filter(parentguid=self.aoguid, livestatus=True)

    def get_path_list(self):
        result = [self, ]

        def build_path(addrobjlist):
            for addrobj in addrobjlist:
                result.append(addrobj)
                build_path(addrobj.get_parent())

        build_path(self.get_parent())
        return result

    def get_path(self):
        result = self.get_path_list()
        return u' > '.join([x.__unicode__() for x in result])


class House(models.Model):
    u"""HOUSE (House) – содержит записи с номерами домов улиц городов и населенных пунктов,
    номера земельных участков и т.п..
    """
    houseid = models.CharField(
        max_length=36,
        verbose_name=u'Уникальный идентификатор записи дома',
        primary_key=True,
    )
    houseguid = models.CharField(
        max_length=36,
        verbose_name=u'Глобальный уникальный идентификатор дома',
        blank=True, null=True,
        db_index=True,
    )
    aoguid = models.CharField(
        max_length=36,
        verbose_name=u'Guid записи родительского объекта (улицы, города, населенного пункта и т.п.)',
        blank=True, null=True,
        db_index=True,
    )

    postalcode = models.CharField(max_length=6, verbose_name=u'Почтовый индекс', blank=True, null=True)
    housenum = models.CharField(max_length=20, verbose_name=u'Номер дома', blank=True, null=True, db_index=True)
    eststatus = models.IntegerField(choices=ESTSTATUS_CHOICES, verbose_name=u'Признак владения')
    strstatus = models.IntegerField(choices=STRSTATUS_CHOICES, verbose_name=u'Признак строения')
    buildnum = models.CharField(max_length=10, verbose_name=u'Номер корпуса', blank=True, null=True)
    strucnum = models.CharField(max_length=10, verbose_name=u'Номер строения', blank=True, null=True)

    startdate = models.DateField(verbose_name=u'Начало действия записи')
    updatedate = models.DateField(verbose_name=u'Дата внесения записи')
    enddate = models.DateField(verbose_name=u'Окончание действия записи')
