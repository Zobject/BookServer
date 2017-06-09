#coding:utf8
from django.conf.urls import url,include
from django.contrib import admin
from Test import views
from DjangoUeditor import urls as DjangoUeditor_urls
urlpatterns = [
    #后台添加页面 bookcover 读物  listen 音频文件
    url(r'^admin/', admin.site.urls),
    url(r'^addbook/', views.addbook),
    url(r'^addlisten/', views.addlisten),

    #bookcover API接口
    url(r'^getbooklist/$', views.booklist),
    url(r'^bookdetails/$', views.bookdetails),


    #用户接口
    url(r'^createuserinfo/$', views.createuserinfo),
    url(r'^getuserlove/$', views.getuserlove),
    url(r'^createuserlove/$', views.createuserlove),
    url(r'^removeuserlove/$', views.removeuserlove),




    #听书接口
    url(r'^listenlist/$', views.listenlist),
    url(r'^listendetails/$', views.listendetails),





    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'freemusic/',views.freemusic),
]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)