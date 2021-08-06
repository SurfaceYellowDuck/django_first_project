from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from adminapp.forms import CategoryForm, ProductForm, AdminOrderItemEditForm, AdminOrderForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test

from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')


class UserCreateView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = "adminapp/user_create.html"
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователи/создать'

        return context


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')
    form_class = ShopUserEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        context['fields'] = ('username', 'first_name', 'last_name', 'email', 'age')
        return context


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


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    form_class = CategoryForm
    template_name = "adminapp/category_create.html"
    success_url = reverse_lazy('admin_staff:categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data()
        context['title'] = 'категории/создать'

        return context


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


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin_staff:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/'
        context['category_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        products = Product.objects.filter(category__pk=self.kwargs['pk']).order_by('is_deleted')
        return products


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


class ProductReadView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


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


class OrdersView(ListView):
    model = Order
    # fields = ('status',)
    template_name = 'adminapp/order_list.html'
    def get_queryset(self):
        return Order.objects.all()


class AdminOrderCreate(CreateView):
    model = Order
    fields = []
    context_object_name = 'object'
    template_name = 'adminapp/order_create.html'
    success_url = reverse_lazy('adminapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(AdminOrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=AdminOrderForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
                basket_items = Basket.objects.filter(user=self.request.user)
                basket_items.delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(AdminOrderCreate, self).form_valid(form)


class AdminOrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    fields = []
    context_object_name = 'object'
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(AdminOrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=AdminOrderItemEditForm, extra=1)
        # basket_items = Basket.objects.filter(user=self.request.user)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            # if self.object.status == "PD":
                 # basket_items.delete()
            data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(AdminOrderUpdate, self).form_valid(form)
