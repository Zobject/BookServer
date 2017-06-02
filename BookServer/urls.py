from django.conf.urls import url,include
from django.contrib import admin
from Test import views
from DjangoUeditor import urls as DjangoUeditor_urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ok/', views.index),
    url(r'^upload/', views.musicurl),


    url(r'^getbooklist/$', views.booklist),
    url(r'^bookdetails/$', views.bookdetails),

    url(r'^createuserinfo/$', views.createuserinfo),
    url(r'^getuserlove/$', views.getuserlove),
    url(r'^createuserlove/$', views.createuserlove),
    url(r'^removeuserlove/$', views.removeuserlove),


    url(r'^listenlist/$', views.listenlist),
    url(r'^listendetails/$', views.listendetails),
    url(r'^upload/$', views.listendetails),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)