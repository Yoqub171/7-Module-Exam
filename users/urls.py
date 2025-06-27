from django.urls import path
from .views import LoginPage, RegisterPage, logout_page, activate

app_name = 'users'

urlpatterns = [
    path('login_page/', LoginPage.as_view(), name='login_page'),
    path('logout_page/', logout_page, name='logout_page'),
    path('register_page/', RegisterPage.as_view(), name='register_page'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

]