from basketapp.models import Basket


def basket(request):
    _basket = []
    if request.user.is_authenticated:
        _basket = request.user.basket.select_related()
    return {
        'basket': _basket,
    }
