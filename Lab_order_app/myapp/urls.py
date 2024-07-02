from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('patient/', views.patient, name='patient'),
    path('lab/', views.lab, name='lab'),
    path('doctor/', views.doctor, name='doctor'),
]