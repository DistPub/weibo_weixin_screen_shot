from django.views.generic import TemplateView


class WeiboCaptureView(TemplateView):
    template_name = 'web/capture.html'
