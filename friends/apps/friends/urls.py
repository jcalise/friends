from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name="register"),
    url(r'^main$', views.main, name="main"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^(?P<id>\d{1,50})/add$', views.add, name="add"),
    url(r'^(?P<id>\d{1,50})/view$', views.view, name="view"),
    url(r'^(?P<id>\d{1,50})/remove$', views.remove, name="remove")
    # url(r'^create$', views.create, name="create"),
    # url(r'^(?P<id>\d{1,50})/destroy$', views.destroy, name="destroy"),
    # url(r'^(?P<id>\d{1,50})/update$', views.update, name="update")
]