import json

from django.shortcuts import render
from django.db.models import Q
from catalog.models import Item, Category
from .forms import Filter


def main(request, categoryId=None):
    # определим пустые выражения для выборки из модели,
    # чтобы в самом простом случае выгрузить все
    queryCategory = Q()
    querySeason = Q()

    data = request.session.get('filterForm', {})
    filterForm = Filter(initial=data)

    # выполняем обработку формы фильтр
    if request.method == 'POST':
        if 'apply' in request.POST:
            filterForm = Filter(request.POST)
        else:
            filterForm = Filter()
        if filterForm.is_valid():
            data = filterForm.cleaned_data
            request.session['filterForm'] = data
        else:
            data = {}
            request.session['filterForm'] = data
            print('form is not valid')

    # сначала определим параметры фильтра по размеру, если задан
    minSize = Item.objects.order_by('size')[0].size
    maxSize = Item.objects.order_by('-size')[0].size
    print(str(minSize) + '-' + str(maxSize))

    sizeFrom = data.get('sizeFrom', minSize)
    if sizeFrom is None:
        sizeFrom = minSize

    sizeTo = data.get('sizeTo', maxSize)
    if sizeTo is None:
        sizeTo = maxSize

    print(str(sizeFrom) + '-' + str(sizeTo))

    querySize = Q(size__range=(sizeFrom, sizeTo))

    # теперь определим параметры фильтра по сезону
    seasonsName = []
    for season in filterForm.fields:
        if season not in filterForm.sizeList:
            if data.get(season, False):
                seasonsName.append(season)

    # если никакой сезон не выбран, значит включаем все
    if len(seasonsName):
        querySeason = Q(season__name__in=seasonsName)

    if categoryId:
        category = Category.objects.get(id=categoryId)
        if category.parentId is None:
            queryCategory = Q(categoryId__parentId=categoryId)
        else:
            queryCategory = Q(categoryId=categoryId)

    items = Item.objects.filter(queryCategory & querySize & querySeason)

    # вытягиваем все родительские категории
    categories = Category.objects.filter(parentId=None)
    inners = []

    if categoryId is not None:
        category = Category.objects.get(id=categoryId)
        if category.parentId is not None:
            inners = Category.objects.filter(parentId=category.parentId)
        else:
            inners = Category.objects.filter(parentId=category.id)

    history = []

    isActive = categoryId is None

    while categoryId is not None:
        category = Category.objects.get(id=categoryId)
        history.insert(0, category)
        categoryId = category.parentId

    topMenu = [
        {"name": "На главную", "active": isActive, "href": "/"},
        {"name": "Добавить категорию", "active": False, "href": "/edit/category"},
        {"name": "Добавить запись", "active": False, "href": "/edit/item"},
    ]

    return render(request, 'main.html',
                  {'items': items, 'categories': categories, 'inners': inners,
                   'history': history, 'filterForm': filterForm, 'topMenu': topMenu})
