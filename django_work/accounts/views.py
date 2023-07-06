from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import LoginAuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class AccountCreateView(generic.CreateView):
    Model = User
    form_class = UserCreationForm
    template_name = 'accounts/accounts_create.html'
    success_url = "/accounts/login"


class Login(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginAuthenticationForm


class Logout(LogoutView):
    next_page = '/accounts/login'

