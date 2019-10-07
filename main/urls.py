from django.conf.urls import *
from django.urls import path
from . import views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path(r'blog/', views.blog, name='blog'),
    url(r'^blog/article', views.blogArticle, name='blogArticle'),
    path(r'faq/', views.faq, name='faq'),
    path(r'about/', views.about, name='about'),
    path(r'support/', views.support, name='support'),
    url(r'^transfer/$', views.transfer, name='transfer'),
    path(r'style2paint/', views.style2paint, name='style2paint'),
    path(r'login/', views.user_login, name='user_login'),
    # path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    path(r'register/', views.register, name='register'),
    path(r'playground/', views.playground, name='playground'),
    path(r'tip/', views.tip, name='tip'),
    path(r'showImage/', views.showImg, name='showImg'),
    url(r'^ajaxUpload/$', views.ajaxUpload, name='ajaxUpload'),
]
