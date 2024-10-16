from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('all_playgrounds/', views.AllPlayGrounds.as_view(), name='all_playgrounds'),
    path('add_playground/', views.AddPlayGrounds.as_view(), name='add_playground'),
    path('contact/', views.HomePage.as_view(), name='contact'),
    path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),
    path('sport_ground/<slug:sportground_slug>/', views.ShowSportGround.as_view(), name='sport_ground'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterCreateUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name="SportsGrounds/password_change_done.html"), name='password_change_done'),
    ]
