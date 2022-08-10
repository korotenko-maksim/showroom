from django.db import models


class Category(models.Model):
    parentId = models.IntegerField(null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Categories"


class Season(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Seasons"


class Producer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Producers"


class Item(models.Model):
    categoryId = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    producer = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Items"
