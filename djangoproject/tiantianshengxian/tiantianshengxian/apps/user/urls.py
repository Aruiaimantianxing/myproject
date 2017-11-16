# coding=utf-8
from django.conf.urls import url
from user.views import Register,ActicateView,LoginView

urlpatterns = [
    url(r'^/',Register.as_view()),
    url(r'^register', Register.as_view(), name='register'),
    # url(r'^active/(?p<token>.*)',ActicateView.as_view(),name='active')
    url(r'^active/(?P<token>.*)', ActicateView.as_view(), name='active'),
    url(r'^login', LoginView.as_view(), name='login'),

]
