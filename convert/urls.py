from django.conf.urls import patterns, url
from convert import views

urlpatterns = patterns('',
        url(r'^$', views.uploader, name='upload'),
		url(r'^dmidi', views.dloadmidi, name='dmidi'),
		url(r'^dpdf', views.dloadpdf, name='dpdf'),
)
