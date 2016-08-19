from django.conf.urls import url
from . import views           

urlpatterns = [
url(r'^$', views.index, name="index"),
url(r'^user/create$', views.create_user, name="create_user"),
url(r'^user/login$', views.login, name="login"),
url(r'^travels$', views.showtravel, name="showtravel"),
url(r'^user/logout$', views.logout, name="logout"),
url(r'^travel/edit$', views.edittravel, name="edittravel"),
url(r'^travel/update$', views.updatetravel, name="updatetravel"),
url(r'^travel/join/(?P<travelid>\d+)$', views.jointravel, name="jointravel"),
url(r'^travel/destination/(?P<travelid>\d+)$', views.showdestination, name="showdestination"),          
	]