#coding:utf8
from django.conf.urls import url,include
from django.contrib import admin
from Test import views
from DjangoUeditor import urls as DjangoUeditor_urls
urlpatterns = [
    #后台添加页面 bookcover 读物  listen 音频文件  添加 music freemusic
    url(r'^admin/', admin.site.urls),
    url(r'^addbook/', views.addbook),
    url(r'^addlisten/', views.addlisten),
    url(r'^addmusic',views.addmusic),
    url(r'^freedelet/$',views.freedelet),
    url(r'^freechange/$',views.freechange),
    url(r'^changesomething/$',views.changesomething),
    url(r'^changesome/$',views.changesome),


    #添加音乐接口到android
    url(r'^android/$',views.addmusicandroid),
    #anroid 请求接口
    url(r'^getfreemusicandroid',views.freemusicandroid),




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


    url(r'^test',views.test),


    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    url(r'^freemusic/',views.freemusic),

    url(r'^showbooklist',views.showbooklist),
    url(r'^changebookcontent',views.changebookcontent),
    url(r'^acceptbookcontent',views.acceptbookcontent),
    url(r'^addphoto',views.addphoto),


    #更改听书接口

    url(r'^changelistensome/$',views.changelistensome),
    url(r'^listenchange/$',views.listenchange),
]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)