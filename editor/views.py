from django.shortcuts import render
from .forms import *
from catalog.models import Category
from django.db import models


def editCategory(request):
    if request.method == 'POST':
        form = EditCategory(data=request.POST)

        if form.is_valid():
            print('form is valid')
            data = form.cleaned_data
            category = Category(name=data['name'])
            if data['isSubGroup']:
                category.parentId = data['parentId']
            category.save()
        else:
            print('form is not valid')

    form = EditCategory()
    return render(request, 'editor.html', {'form': form})


def editItem(request):
    if request.method == 'POST':
        form = EditItem(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            category = Category.objects.only('id').get(id=data['category'])
            season = Season.objects.only('id').get(id=data['season'])
            item = Item(name=data['name'], categoryId=category, size=data['size'],
                        season=season, producer=data['producer'])
            item.save()
    form = EditItem()
    return render(request, 'editor.html', {'form': form})
