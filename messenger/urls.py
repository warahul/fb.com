from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.Sitelogin, name='Sitelogin'),
        url(r'^chooseuser/$', views.chooseuser, name='chooseuser'),
    url(r'^(?P<response>[0-9]+)/results/$', views.results, name='results'),
]

