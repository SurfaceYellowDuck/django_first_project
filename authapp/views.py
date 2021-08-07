from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.conf import settings
from .models import ShopUser
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView


# from django.contrib.auth.mixins import LoginRequiredMixin


# class ProductCategoryUpdateView(UpdateView):
#     model = ProductCategory
#     template_name = 'adminapp/category_update.html'
#     success_url = reverse_lazy('admin_staff:categories')
#     form_class = CategoryForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'категории/редактирование'
#         context['fields'] = '__all__'
#
#         return context
#
# class login()
def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале \
    {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user {user.username}')
            return render(request, 'authapp/verification.html')
    except Exception as err:
        print(f'error activation user {err.args}')
        return HttpResponseRedirect(reverse('index'))


class UserLoginView(LoginView):
    form_class = ShopUserLoginForm
    template_name = 'authapp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['next'] = self.request.GET['next'] if 'next' in self.request.GET.keys() else ''
        context['fields'] = '__all__'
        return dict(list(context.items()))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))
        else:
            self.form_invalid(form)
            return HttpResponseRedirect(reverse('index'))

# def login(request):
#     title = 'вход'
#
#     login_form = ShopUserLoginForm(data=request.POST)
#
#     _next = request.GET['next'] if 'next' in request.GET.keys() else ''
#
#     if request.method == 'POST' and login_form.is_valid():
#         username = request.POST['username']
#         password = request.POST['password']
#
        # user = auth.authenticate(username=username, password=password)
        # if user and user.is_active:
        #     auth.login(request, user)
        #     if 'next' in request.POST.keys():
        #         return HttpResponseRedirect(request.POST['next'])
        #     else:
        #         return HttpResponseRedirect(reverse('index'))
#
#     context = {
#         'title': title,
#         'login_form': login_form,
#         'next': _next,
#     }
#     return render(request, 'authapp/login.html', context)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

class UserRegistrationView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = "authapp/register.html"
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['title'] = 'пользователи/создать'
        context['fields'] = '__all__'

        return context

    def get_form_class(self):
        return self.form_class

    def post(self, request, *args, **kwargs):
        user = self.get_form().save()
        if send_verify_email(user):
            print('сообщение подтверждения отправлено')
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            print('ошибка отправки сообщения')
            return HttpResponseRedirect(reverse('auth:login'))

# def register(request):
#     title = 'регистрация'
#
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(request.POST, request.FILES)
#
#         if register_form.is_valid():
#             user = register_form.save()
#             if send_verify_email(user):
#                 print('сообщение подтверждения отправлено')
#                 return HttpResponseRedirect(reverse('auth:login'))
#             else:
#                 print('ошибка отправки сообщения')
#                 return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         register_form = ShopUserRegisterForm()
#
#     content = {'title': title, 'register_form': register_form}
#
#     return render(request, 'authapp/register.html', content)


# class UserEditView(UpdateView):
#     model = ShopUser
#     template_name = 'authapp/edit.html'
    # success_url = reverse_lazy('index')

    # def get_full_form(self):
    #     form_class_1 = formset_factory(ShopUserEditForm)
    #     form_class_2 = formset_factory(ShopUserProfileEditForm)
    #     full_form = []
    #     for el in form_class_2():
    #         full_form.append(el.as_table())
    #     for el in form_class_1():
    #         full_form.append(el.as_table())
    #     for el in full_form:
    #         return full_form

    # form_class = get_full_form()
    # fields = ('username', 'first_name', 'last_name', 'email', 'age')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form_class'] = self.get_full_form()
    #     context['title'] = 'пользователи/редактирование'
    #     context['fields'] = '__all__'
    #     return context
    #
    # def get_success_url(self):
    #     return reverse_lazy('authapp:edit', args=[self.request.user.pk])
@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }

    return render(request, 'authapp/edit.html', context)
