from django.shortcuts import render
from django.db.models import Q
from catalog.models import Item, Category
from .forms import Filter


def main(request, categoryId=None):
    # выполняем обработку формы фильтр
    querySize = Q()
    querySeason = Q()
    if request.method == 'POST':
        filterForm = Filter(request.POST)
        if filterForm.is_valid():
            data = filterForm.cleaned_data

            # сначала определим параметры фильтра по размеру, если задан
            if data['sizeFrom'] is None:
                data['sizeFrom'] = 0
            if data['sizeTo'] is None:
                data['sizeTo'] = 1000

            querySize = Q(size__range=(data['sizeFrom'], data['sizeTo']))

            # теперь определим параметры фильтра по сезону
            seasonsName = []
            for season in filterForm.fields:
                if season not in filterForm.sizeList:
                    if data[season]:
                        seasonsName.append(season)

            # если никакой сезон не выбран, значит включаем все
            if len(seasonsName):
                querySeason = Q(season__name__in=seasonsName)
        else:
            print('form is not valid')
    else:
        filterForm = Filter()

    if categoryId is None:
        items = Item.objects.filter(querySize & querySeason)
    else:
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
