from django import forms
from catalog.models import Category


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
