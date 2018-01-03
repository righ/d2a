# coding: utf-8

import uuid
from django.db import models


class CategoryRelation(models.Model):
    category1 = models.ForeignKey('demo.Category', related_name='parents', on_delete=models.CASCADE)
    category2 = models.ForeignKey('demo.Category', related_name='children', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'category_relation'


class Author(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'author'


class Category(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    related_coming = models.ManyToManyField('self', symmetrical=False,
                                            through='CategoryRelation', related_name='related_going')

    class Meta:
        db_table = 'category'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='books')
    category = models.ManyToManyField(Category, related_name='books')

    class Meta:
        db_table = 'book'

class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sales')
    sold = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sales'

