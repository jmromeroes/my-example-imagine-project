from django.db import models


class M1(models.Model):

    id = models.AutoField(primary_key=True)
    m2s = models.ManyToManyField('M2', related_name='m1s', db_table='m1_m2', blank=True)

    class Meta:
        db_table = "m1"


class M2(models.Model):

    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "m2"
