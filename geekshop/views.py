from django.shortcuts import render
import json

from basketapp.models import Basket

# page_header = [
#         {'page_name': 'contacts', 'header': 'НАШИ КОНТАКТЫ'},
#         {'page_name': 'index', 'header': 'УДОБНЫЕ СТУЛЬЯ'},
# ]


def read_json(way_to_file):
    with open(way_to_file) as tables:
        chairs_json = json.load(tables)
        # print(chairs_json)
        chairs_list = []
        for section, commands in chairs_json.items():
            chairs_list = commands
        print(chairs_list)
        return chairs_list


def index(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    title = 'магазин'
    tables = read_json(r'C:\Learning_Django\django_first_project\tables.json')
    context = {
        'title': title,
        # 'page_header': page_header,
        'tables': tables,
        'basket': basket
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'basket': basket
    }
    return render(request, 'geekshop/contact.html', context=context)
