"""
URL configuration for djangoweb230502 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from board import views

urlpatterns = [
    path("", views.home),
    path("cctv_map/", views.cctv),
    path("wordcloud/", views.wordcloud),
    #관리자용 사이트
    path("admin/", admin.site.urls),
    #게시판 관련 url
    path("list/", views.list),
    path("write/", views.write),
    path("insert/", views.insert),
    path("detail/", views.detail),
    path("update/", views.update),
    path("delete/", views.delete),
    path("download/", views.download),
    path("reply_insert/", views.reply_insert),
    path("signup_form/", views.signup_form),
    path("signup/", views.signup),
    path("login_form/", views.login_form),
    path("login/", views.login),
    path("logout/", views.logout),
]


