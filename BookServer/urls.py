"""BookServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Test import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ok/', views.index),
    url(r'^insert/', views.insert),
    #url(r'^upload/', views.musicurl),


    url(r'^getbooklist/$', views.booklist),
    url(r'^bookdetails/$', views.bookdetails),

    url(r'^createuserinfo/$', views.createuserinfo),
    url(r'^getuserlove/$', views.getuserlove),
    url(r'^createuserlove/$', views.createuserlove),



    url(r'^listenlist/$', views.listenlist),
    url(r'^listendetails/$', views.listendetails),
    url(r'^upload/$', views.listendetails),
]
