from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    # url(r'^new$', views.new, name="new"),
    # url(r'^(?P<id>\d{1,50})/edit$', views.edit, name="edit"),
    # url(r'^(?P<id>\d{1,50})$', views.show, name="show"),
    # url(r'^create$', views.create, name="create"),
    # url(r'^(?P<id>\d{1,50})/destroy$', views.destroy, name="destroy"),
    # url(r'^(?P<id>\d{1,50})/update$', views.update, name="update")
]