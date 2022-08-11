from django import forms
from catalog.models import *


class EditCategory(forms.Form):
    name = forms.CharField(label='Наименование')
    isSubGroup = forms.BooleanField(label='Подкатегория', required=False)
    parentId = forms.ChoiceField(label='Категория', required=True, initial=None)

    def __init__(self, *args, **kwargs):
        super(EditCategory, self).__init__(*args, **kwargs)
        # читаем базу, формируя кортеж choices
        choices = []
        for category in Category.objects.filter(parentId=None):
            choices.append((category.id, category.name))
        self.fields['parentId'].choices = choices


class EditItem(forms.Form):
    name = forms.CharField(label='Наименование')
    category = forms.ChoiceField(label='Категория')
    size = forms.IntegerField(label='Размер')
    season = forms.ChoiceField(label='Сезон')
    producer = forms.CharField(label='Производитель')
    image = forms.ImageField(label='Изображение', max_length=255)

    def __init__(self, *args, **kwargs):
        super(EditItem, self).__init__(*args, **kwargs)

        # init category field
        categories = []
        for category in Category.objects.filter(parentId=None):
            group = []
            for subGroup in Category.objects.filter(parentId=category.id):
                group.append((subGroup.id, subGroup.name))
            categories.append((category.name, group))
        self.fields['category'].choices = categories

        # init season field
        seasons = []
        for season in Season.objects.all():
            seasons.append((season.id, season.name))
        self.fields['season'].choices = seasons
