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
        filterForm = Filter(request.POST)
        if filterForm.is_valid():
            data = filterForm.cleaned_data
            request.session['filterForm'] = data
        else:
            print('form is not valid')

    # сначала определим параметры фильтра по размеру, если задан
    sizeFrom = data.get('sizeFrom', 0)
    if sizeFrom is None:
        sizeFrom = 0
    sizeTo = data.get('sizeTo', 1000)
    if sizeTo is None:
        sizeTo = 1000

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

    while categoryId is not None:
        category = Category.objects.get(id=categoryId)
        history.insert(0, category)
        categoryId = category.parentId

    return render(request, 'main.html',
                  {'items': items, 'categories': categories, 'inners': inners,
                   'history': history, 'filterForm': filterForm})
