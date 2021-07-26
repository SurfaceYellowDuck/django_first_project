from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegistrationView, UserEditView, send_verify_email, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('edit/<int:pk>', UserEditView.as_view(), name='edit'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify')
    ]
