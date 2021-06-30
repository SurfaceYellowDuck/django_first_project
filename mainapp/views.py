from django.shortcuts import render
from .models import Product, ProductCategory


def categorys(request):
    title = 'главная'
    products = Product.objects.all()
    categorys = ProductCategory.objects.all()
    context = {
        'title': title,
        'products': products,
        'categorys': categorys,
    }
    return render(request, template_name='mainapp/test.html', context=context)


def products(request, pk=None):
    print(pk)
    title = 'продукты/каталог'
    links_menu = [
        {'href': 'products_all', 'name': ProductCategory.objects.get(name='Всё')},
        {'href': 'products_home', 'name': ProductCategory.objects.get(name='Дом')},
        {'href': 'products_office', 'name': ProductCategory.objects.get(name='Офис')},
        {'href': 'products_modern', 'name': ProductCategory.objects.get(name='Модерн')},
        {'href': 'products_classic', 'name': ProductCategory.objects.get(name='Классика')},
    ]
    context = {
        'title': title,
        'links_menu': links_menu,

    }

    return render(request=request, template_name='mainapp/products.html', context=context)
