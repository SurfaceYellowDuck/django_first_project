from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from basketapp.models import Basket, total_price, total_quantity
from mainapp.models import Product


def basket(request):
    price = total_price()
    quantity = total_quantity()
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        context = {
            'basket': basket,
            'price': price,
            'quantity': quantity
        }
        return render(request, 'basketapp/basket.html', context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated != True:
        return HttpResponseRedirect(reverse('auth:login'))
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, pk):
    return render(request, 'basketapp/basket.html')
