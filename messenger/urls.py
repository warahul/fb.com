from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.Sitelogin, name='Sitelogin'),
    url(r'^chooseuser/$', views.chooseuser, name='chooseuser'),
    url(r'^sendMesg$', views.sendMesg, name='sendMesg'),
    url(r'^getMsg$', views.getMsg, name='getMsg'),
    url(r'^(?P<response>[0-9]+)/results/$', views.results, name='results'),
]

