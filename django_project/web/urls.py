from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^weibo/capture/$',
        views.WeiboCaptureView.as_view(), name='weibo-capture'),
    url(r'^weibo/capture/(?P<base64_media_path>\w+)/$',
        views.WeiboCaptureResultView.as_view(), name='weibo-capture-result'),
]
