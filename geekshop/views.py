from django.shortcuts import render
import json
page_header = [
        {'page_name': 'contacts', 'header': 'НАШИ КОНТАКТЫ'},
        {'page_name': 'index', 'header': 'УДОБНЫЕ СТУЛЬЯ'},
]


def read_json(way_to_file):
        with open(way_to_file) as tables:
            chairs_json = json.load(tables)
        # print(chairs_json)
        chairs_list = []
        for section, commands in chairs_json.items():
            chairs_list = commands
        print(chairs_list)
        return chairs_list
# read_json(r'C:\Learning_Django\learn_django_beginner\lesson2\geekshop\tables.json')


def index(request):
    title = 'магазин'
    tables = read_json(r'C:\Learning_Django\learn_django_beginner\lesson2\geekshop\tables.json')
    context = {
        'title': title,
        'page_header': page_header,
        'tables': tables,
    }
    return render(request, 'geekshop/index.html', context=context)


def contacts(request):
    context = {
        'page_header': page_header
    }
    return render(request, 'geekshop/contact.html', context=context)
