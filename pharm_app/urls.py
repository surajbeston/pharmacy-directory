from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('signup-pharma', views.signup_pharma),
    path('signin-pharma', views.signin_pharma),
    path('home', views.home),
    path('search', views.medicine_search),
    re_path(r'^activate/(?P<activation_code>.+)$', views.activate, name='activate'),
    re_path(r'^finish/(?P<key>.+)$', views.finish, name='finish'),
    re_path(r'^delete/(?P<key>.+)$', views.delete, name='delete'),
    re_path(r'^add-composition/(?P<key>.+)$', views.add_composition, name='add_composition'),
    re_path(r'^auth_download/(?P<key>.+)$', views.auth_download, name='download')
]
