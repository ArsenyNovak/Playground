from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.HomePage.as_view(), name='about'),
    path('all_playgrounds/', views.HomePage.as_view(), name='all_playgrounds'),
    path('add_playground/', views.HomePage.as_view(), name='add_playground'),
    path('contact/', views.HomePage.as_view(), name='contact'),
    ]