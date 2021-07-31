from django.urls import path
import adminapp.views as adminapp
from adminapp.views import UsersListView, UserCreateView, UsersUpdateView, ProductCategoryUpdateView, UserDeleteView, \
    ProductCategoryCreateView, ProductCategoryView, ProductCategoryDeleteView, ProductListView, ProductCreateView, \
    ProductReadView, ProductUpdateView, ProductDeleteView, OrdersView, OrderCreate

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/read/', UsersListView.as_view(), name='users'),
    path('users/update/<int:pk>/', UsersUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', ProductCategoryView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', ProductCategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/', ProductCreateView.as_view(), name='product_create'),
    path('products/read/category/<int:pk>/', ProductListView.as_view(), name='products'),
    path('products/read/<int:pk>/', ProductReadView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('orders/', OrdersView.as_view(), name='orders_list'),
    path('orders/create/', OrderCreate.as_view(), name='order_create'),
    # path('orders/update/<int:pk>/', OrderUpdate.as_view(), name='order_update'),
]