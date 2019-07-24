""" URLS for blog functions """

from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blogsite import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('<single_slug>', views.single_slug, name='single_slug'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('my_blogs/', views.my_blogs, name='my_blogs'),
    path('my_blogs/<single_slug>', views.edit_blog, name='edit_blog'),
]

urlpatterns += staticfiles_urlpatterns()

