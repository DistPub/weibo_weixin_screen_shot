import base64
import os
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView
from selenium.common.exceptions import TimeoutException

from django_project import utils

from web.forms import WeiboCaptureRequestForm
from web.services import WeiboCaptureService


class WeiboCaptureView(FormView):
    """
    weibo capture view
    """
    template_name = 'web/capture.html'
    form_class = WeiboCaptureRequestForm

    def form_valid(self, form):
        """
        When form valid, save it to view
        """
        url = form.cleaned_data['url']
        service = WeiboCaptureService(url)
        self.user_media_path = utils.generate_user_media_image_path(name='capture', prefix='weibo')
        file_path = os.path.join(settings.MEDIA_ROOT, self.user_media_path)
        try:
            service.capture_to_file(file_path)
        except TimeoutException:
            os.remove(file_path)
            self.user_media_path = settings.DEFAULT_WEIBO_CAPTURE_IMAGE
        return super(WeiboCaptureView, self).form_valid(form)

    def get_success_url(self):
        """
        Return success url
        """
        base64_media_path = base64.b64encode(self.user_media_path)
        return reverse('web:weibo-capture-result', kwargs={'base64_media_path': base64_media_path})


class WeiboCaptureResultView(TemplateView):
    """
    weibo capture result view
    """
    template_name = 'web/capture_result.html'

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super(WeiboCaptureResultView, self).get_context_data()
        context['image_url'] = self._get_weibo_capture_image_url(self.kwargs['base64_media_path'])
        return context

    def _get_weibo_capture_image_url(self, base64_media_path):
        """
        Return weibo capture image url
        :param base64_media_path: user media file path base64 encrypt string
        """
        relative_url = WeiboCaptureService.get_media_relative_path_by(base64_media_path)
        return self.request.build_absolute_uri(relative_url)
