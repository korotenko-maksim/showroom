from django.db import models


class Category(models.Model):
    parentId = models.IntegerField()
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'Categories'
