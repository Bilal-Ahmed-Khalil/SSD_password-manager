from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('confirm/', views.confirm_code, name='confirm'),
    path('add-password/', views.add_password, name='add_password'),
    path('update/<int:id>/', views.update_password, name='update_password'),
]