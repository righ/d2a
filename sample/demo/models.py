import uuid
from django.db import models


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    no = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, null=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'test_table'
