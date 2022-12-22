from django.shortcuts import render
from .forms import *
from catalog.models import Category
from django.db import models

topMenu = [
    {"name": "На главную", "active": False, "href": "/"},
    {"name": "Добавить категорию", "active": False, "href": "/edit/category"},
    {"name": "Добавить запись", "active": False, "href": "/edit/item"},
]


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
    topMenu[1]['active'] = True
    topMenu[2]['active'] = False
    return render(request, 'editor.html', {'form': form, 'topMenu': topMenu, 'title': 'ДОБАВИТЬ КАТЕГОРИЮ'})


def editItem(request):
    if request.method == 'POST':
        form = EditItem(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            category = Category.objects.only('id').get(id=data['category'])
            season = Season.objects.only('id').get(id=data['season'])
            item = Item(name=data['name'], categoryId=category, size=data['size'],
                        season=season, producer=data['producer'])
            item.image = data['image']
            item.save()
        else:
            print(form.errors)
    form = EditItem()
    topMenu[1]['active'] = False
    topMenu[2]['active'] = True
    return render(request, 'editor.html', {'form': form, 'topMenu': topMenu, 'title': 'ДОБАВИТЬ ЗАПИСЬ'})
