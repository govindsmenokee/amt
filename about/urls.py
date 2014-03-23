from django.conf.urls import patterns, url
from about import views

urlpatterns = patterns('',
        url(r'^$', views.aboutpage, name='about'))
