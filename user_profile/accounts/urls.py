from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('password/', views.change_password, name='password'),
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
]