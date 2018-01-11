# coding: utf-8
import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


class CategoryRelation(models.Model):
    category1 = models.ForeignKey('Category', related_name='parents', on_delete=models.CASCADE)
    category2 = models.ForeignKey('Category', related_name='children', on_delete=models.CASCADE)
    type = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'postgresql_category_relation'


class Author(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'postgresql_author'


class Category(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    related_coming = models.ManyToManyField('self', symmetrical=False,
                                            through='CategoryRelation', related_name='related_going')

    class Meta:
        db_table = 'postgresql_category'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = JSONField()
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name='books')
    content = models.BinaryField()
    category = models.ManyToManyField(Category, related_name='books')
    tags = ArrayField(models.CharField(max_length=10), size=3)

    class Meta:
        db_table = 'postgresql_book'


class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sales')
    sold = models.DateTimeField(auto_now_add=True)
    reservation = models.DurationField(null=True)
    source = models.GenericIPAddressField(null=True)

    class Meta:
        db_table = 'postgresql_sales'

