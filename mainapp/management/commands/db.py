from django.core.management.base import BaseCommand
import json
import os
from pathlib import Path
from mainapp.models import Product, ProductCategory
import re


def read_json(way_to_file):
    with open(way_to_file) as tables:
        chairs_json = json.load(tables)
    # print(chairs_json)
    chairs_list = []
    for section, commands in chairs_json.items():
        chairs_list = commands
    print(chairs_list)
    return chairs_list
read_json(r'C:\Learning_Django\learn_django_beginner\lesson2\geekshop\tables.json')




# def fill_db():
#     json_massive = read_json(r'tables.json')
#     for el in json_massive:
#         search_element = re.search(r'стул', el)
#         if ProductCategory.objects.get('Классика'):
#             new_product = Product.objects.name(name=el, category=ProductCategory.objects.get('Классика'))
#             new_product.save()
# print(project_dir)
# read_json('tables.json')
# read_json(r'C:\Learning_Django\learn_django_beginner\lesson2\geekshop\tables.json')