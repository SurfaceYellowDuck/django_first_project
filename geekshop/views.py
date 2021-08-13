import json
from django.views.generic import ListView, TemplateView
from basketapp.models import Product


def read_json(way_to_file):
    with open(way_to_file) as tables:
        chairs_json = json.load(tables)
        # print(chairs_json)
        chairs_list = []
        for section, commands in chairs_json.items():
            chairs_list = commands
        print(chairs_list)
        return chairs_list


class IndexView(ListView):
    model = Product
    template_name = 'geekshop/index.html'

    queryset_products = Product.objects.filter(is_deleted=True, category__is_deleted=False).select_related('category')[:3]

    # queryset_basket = ''
    # @method_decorator(login_required())
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated():
    #         queryset_basket = ''
    #         return queryset_basket
    #     else:
    #         queryset_basket = Basket.objects.filter(user=request.user)
    #         return queryset_basket

    extra_context = {'title': 'shop', 'products': queryset_products}



    # def get(self, request, *args, **kwargs):
    #     self.object_list = self.get_queryset()
    #     context = self.get_context_data()
    #     return self.render_to_response(context)

# def index(request):
#     basket = []
#     if request.user.is_authenticated:
#         basket = Basket.objects.filter(user=request.user)
#     title = 'магазин'
#     tables = read_json(r'C:\Learning_Django\django_first_project\tables.json')
#     context = {
#         'title': title,
#         # 'page_header': page_header,
#         'tables': tables,
#         'basket': basket
#     }
#     return render(request, 'geekshop/index.html', context=context)


class ContactsView(TemplateView):
    template_name = 'geekshop/contact.html'

# def contacts(request):
#     basket = []
#     if request.user.is_authenticated:
#         basket = Basket.objects.filter(user=request.user)
#     context = {
#         'basket': basket
#     }
#     return render(request, 'geekshop/contact.html', context=context)
