from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('all_playgrounds/', views.AllPlayGrounds.as_view(), name='all_playgrounds'),
    path('add_playground/', views.AddPlayGrounds.as_view(), name='add_playground'),
    path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),
    path('sport_ground/<slug:sportground_slug>/', views.ShowSportGround.as_view(), name='sport_ground'),
    path('api/playgrounds/<slug:cat_slug>/', views.PlayGroundsApi.as_view(), name='api_playgrounds_list'),
    path('api/category_list/', views.CategoryApiList.as_view(), name='api_category_list'),
    path('api/playgrounds_detail/<slug:sportground_slug>/', views.PlaygroundsApiDetail.as_view(), name='api_playgrounds_detail'),

    ]

