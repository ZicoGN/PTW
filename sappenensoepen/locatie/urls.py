# locatie/urls.py
from django.conf.urls import url
from locatie import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^search/$', views.search),
	url(r'^update/$', views.update),
]
