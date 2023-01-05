from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('likes', views.likes, name='likes'),
    path('login', views.login, name='login'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('upload', views.upload, name='upload'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pf>', views.profile, name='profile'),
]