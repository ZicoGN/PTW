# locatie/urls.py
from django.conf.urls import url
from locatie import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
]

def javascript_settings():
    js_conf = {
        'page_title': 'Home',
    }
    return js_conf