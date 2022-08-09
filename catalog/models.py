from django.db import models


class Category(models.Model):
    parentId = models.IntegerField(null=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Categories'

    def __str__(self):
        return self.name
