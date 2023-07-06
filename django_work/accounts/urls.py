from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('accounts_create/', views.AccountCreateView.as_view(), name='accounts_create'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]