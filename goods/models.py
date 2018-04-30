#coding=utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models



class Category(models.Model):
    cname = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'shop_category'
        ordering = ['id']


class Color(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'shop_color'


class Goods(models.Model):
    gname = models.CharField(max_length=255)
    gdesc = models.CharField(max_length=1024, blank=True, null=True)
    gprice = models.DecimalField(max_digits=10, decimal_places=2)
    goldprice = models.DecimalField(max_digits=10, decimal_places=2)
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryId_id')  # Field name made lowercase.
    def img(self):
        return self.store_set.first().color.value
    def colors(self):
        stores = self.store_set.all()
        colors=[]
        for store in stores:
            color = store.color
            if color not in colors:
                colors.append(color)
        return colors
    def sizes(self):
        stores = self.store_set.all()
        sizes=[]
        for store in stores:
            raw_sizes = store.size.all()
            for size in raw_sizes:
              if size not in sizes:
                    sizes.append(size)
        return  sizes

    class Meta:
        managed = False
        db_table = 'shop_goods'


class Goodsdetails(models.Model):
    value = models.CharField(max_length=100)
    goodsid = models.ForeignKey(Goods, models.DO_NOTHING, db_column='goodsId_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shop_goodsdetails'


class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    desc = models.IntegerField()
    created = models.DateTimeField()
    content = models.TextField()
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_order'


class Size(models.Model):
    value = models.CharField(max_length=255)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'shop_size'


class Store(models.Model):
    count = models.IntegerField()
    color = models.ForeignKey(Color, models.DO_NOTHING)
    goods = models.ForeignKey(Goods, models.DO_NOTHING)
    size = models.ManyToManyField(Size)  # 多对多
    class Meta:
        managed = False
        db_table = 'shop_store'


class StoreSize(models.Model):
    store = models.ForeignKey(Store, models.DO_NOTHING)
    size = models.ForeignKey(Size, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shop_store_size'
        unique_together = (('store', 'size'),)


class User(models.Model):
    user = models.CharField(max_length=254)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'shop_user'
