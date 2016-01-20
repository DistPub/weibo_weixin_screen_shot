from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^weibo/capture/$', views.WeiboCaptureView.as_view(), name='weibo-capture'),
]
