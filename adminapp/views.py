from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from adminapp.forms import ShopUserAdminEditForm, CategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(UsersListView, self).get_context_data()
    #     context['title'] = 'админка/пользователи'
    #     return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = "adminapp/user_create.html"
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователи/создать'

        return context
# def user_create(request):
#     title = 'пользователи/создать'
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {'title': title,
#                'user_form': user_form}
#
#     return render(request, 'adminapp/user_create.html', context)


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    form_class = ShopUserEditForm
    # fields = ('username', 'first_name', 'last_name', 'email', 'age')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        context['fields'] = ('username', 'first_name', 'last_name', 'email', 'age')
        return context


# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'user_form': edit_form,
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#     user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user.is_deleted = True
#         user.is_active = False
#         user.save()
#         # user.delete()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#     context = {
#         'title': title,
#         'user_to_delete': user,
#     }
#     return render(request, 'adminapp/user_delete.html', context)


class ProductCategoryView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('is_deleted')

# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = CategoryForm
    template_name = "adminapp/category_create.html"
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data()
        context['title'] = 'категории/создать'

        return context

# def category_create(request):
#     title = 'категории/создать'
#     if request.method == 'POST':
#         category_form = CategoryForm(request.POST, request.FILES)
#
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         category_form = CategoryForm()
#
#     context = {'title': title,
#                'category_form': category_form}
#
#     return render(request, 'adminapp/category_create.html', context)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        context['fields'] = '__all__'

        return context
# def category_update(request, pk):
#     title = 'категории/редактирование'
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = CategoryForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:categories'))
#     else:
#         edit_form = CategoryForm(instance=edit_category)
#
#     context = {
#         'title': title,
#         'category_form': edit_form,
#     }
#
#     return render(request, 'adminapp/category_update.html', context)


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
# def category_delete(request, pk):
#     title = 'категории/удаление'
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category.is_deleted = True
#         category.save()
#         # category.delete()
#         return HttpResponseRedirect(reverse('admin_staff:categories'))
#     context = {
#         'title': title,
#         'category_to_delete': category,
#     }
#     return render(request, 'adminapp/category_delete.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    # context_object_name = 'objects'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/'
        return context

    def get_queryset(self):
        products = Product.objects.filter(category__pk=self.kwargs['pk']).order_by('is_deleted')
        # category = ProductCategory.objects.filter(pk=self.kwargs['pk'])
        return products

# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     context = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "adminapp/product_create.html"

    success_url = reverse_lazy('admin_staff:products')

    def get_context_data(self,  **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        context['title'] = 'продукты/создать'
        context['fields'] = '__all__'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.kwargs['pk']])

# def product_create(request, pk):
#     title = 'продукты/создать'
#     category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
#     else:
#         product_form = ProductForm(initial={'category': category})
#
#     context = {'title': title,
#                'update_form': product_form,
#                'category': category,
#                }
#
#     return render(request, 'adminapp/product_create.html', context)


class ProductReadView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

# def product_read(request, pk):
#     title = 'продукты/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'title': title,
#         'product': product,
#     }
#     return render(request, 'adminapp/product_read.html', context)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "adminapp/product_update.html"

    success_url = reverse_lazy('admin_staff:products')

    def get_context_data(self,  **kwargs):
        context = super(ProductUpdateView, self).get_context_data()
        context['title'] = 'продукты/редактировать'
        context['fields'] = '__all__'
        return context

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.object.category.pk])


# def product_update(request, pk):
#     title = 'продукты/редактировать'
#     edit_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductForm(request.POST, request.FILES, instance=edit_product)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:products', args=[edit_product.category.pk]))
#     else:
#         edit_form = ProductForm(instance=edit_product)
#
#     context = {'title': title,
#                'update_form': edit_form,
#                'category': edit_product.category,
#                'product': edit_product
#                }
#
#     return render(request, 'adminapp/product_update.html', context)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin_staff:products')

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', args=[self.object.category.pk])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    # def get_success_url(self):
    #     return reverse_lazy('admin_staff:products', args=[self.object.category.pk])

# def product_delete(request, pk):
#     title = 'продукты/удаление'
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product.is_deleted = True
#         # product.is_active = False
#         product.save()
#         # product.delete()
#         return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))
#     context = {
#         'title': title,
#         'product_to_delete': product,
#     }
#     return render(request, 'adminapp/product_delete.html', context)
