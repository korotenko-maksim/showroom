from django.shortcuts import render
from .forms import EditCategory
from catalog.models import Category


def editCategory(request):
    if request.method == 'POST':
        form = EditCategory(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            category = Category(name=data['name'])
            category.save()
    # читаем базу, формируя кортеж choices
    choices = []
    for category in Category.objects.filter(parentId=None):
        choices.append((category.id, category.name))
    form = EditCategory()
    form.fields['parent'].choices = choices
    return render(request, 'editor.html', {'form': form})
