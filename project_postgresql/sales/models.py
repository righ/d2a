# coding: utf-8
import uuid

from django.db import models


class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='sales')
    sold = models.DateTimeField(auto_now_add=True)
    reservation = models.DurationField(null=True)
    source = models.GenericIPAddressField(null=True)

    class Meta:
        db_table = 'sales'
