from django import forms


class EditCategory(forms.Form):
    name = forms.CharField(label='Наименование')
    isSubGroup = forms.BooleanField(label='Подкатегория', required=False)
    parent = forms.ChoiceField(label='Категория', required=False, empty_value=None)
