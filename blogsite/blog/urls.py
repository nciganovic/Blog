""" URLS for blog functions """

from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blogsite import settings
from . import views
#from .views import PostLikeToggle

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('<single_slug>', views.single_slug, name='single_slug'),

    path('<single_slug>/like', views.likes, name='likes'),#NEW

    path('create_blog/', views.create_blog, name='create_blog'),
    path('my_blogs/', views.my_blogs, name='my_blogs'),
    path('my_blogs/<single_slug>', views.edit_blog, name='edit_blog'),
    path('delete_blog/<single_slug>', views.delete_blog, name='delete_blog'),
    path('my_info/', views.my_info, name='my_info'),
    path('change_info/', views.change_info, name='change_info'),
    path('contact/', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
