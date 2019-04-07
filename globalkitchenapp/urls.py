from django.conf.urls import url, include
from django.urls import path

from django.contrib import admin
from globalkitchenapp import views

urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^booking/', views.booking, name='booking'),
  url(r'^about/', views.about, name='about'),
  url(r'^contact/', views.contact, name='contact'),
  url(r'^login/', views.login_user, name='login'),
  url(r'^signup/', views.signup, name='signup'),
  url(r'^selectable/', views.selectable, name='selectable'),
  url(r'^fullcalender/', views.fullcalender, name='fullcalender'), 
  url(r'^logout/', views.user_logout, name='logout'),

  
]
