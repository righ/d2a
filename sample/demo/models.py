# coding: utf-8

import uuid
from django.db import models


class CategoryRelation(models.Model):
    category1 = models.ForeignKey('demo.BookCategory', related_name='parents')
    category2 = models.ForeignKey('demo.BookCategory', related_name='children')
    type = models.CharField(max_length=30)

    class Meta:
        db_table = 'category_relation'


class Author(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallInteger()

    class Meta:
        db_table = 'author'


class BookCategory(models):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    related = models.ManyToMany('self')


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, null=True)
    category = models.ManyToMany(BookCategory, symmetrical=False, through='CategoryRelation')

    class Meta:
        db_table = 'book'


class Sales(models.Model):
    id = models.BigAutoField()
    book = models.ForeignKey(Book)
    sold = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sales'
