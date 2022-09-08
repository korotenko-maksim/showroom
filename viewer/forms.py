from django import forms
from catalog.models import *


class Filter(forms.Form):
    sizeFrom = forms.IntegerField(label="", required=False)
    sizeTo = forms.IntegerField(label="", required=False)
    sizeList = ['sizeFrom', 'sizeTo']

    def __init__(self, *args, **kwargs):
        for season in Season.objects.all():
            self.base_fields[season.name] = forms.BooleanField(label=season.name, required=False)
        super(Filter, self).__init__(*args, **kwargs)
        minSize = Item.objects.order_by('size')[0].size
        maxSize = Item.objects.order_by('-size')[0].size
        sizeFields = ['sizeFrom', 'sizeTo']
        for s in sizeFields:
            self.fields[s] = forms.IntegerField(max_value=maxSize, min_value=minSize,
                                                label="", required=False)
