from django.shortcuts import render
from .forms import EditCategory
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
