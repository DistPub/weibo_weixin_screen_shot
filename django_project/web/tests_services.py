import base64

import os
from django.conf import settings
from django.templatetags.static import static
from django.test import TestCase

from web.services import WeiboCaptureService, BrowserService


class BrowserServiceTest(TestCase):
    """
    Test for BrowserService
    """
    def test_instance_property(self):
        service = BrowserService()
        self.assertTrue(hasattr(service, 'screen'))
        self.assertTrue(hasattr(service, 'browser'))


class WeiboCaptureServiceTest(TestCase):
    """
    Test for WeiboCaptureService
    """
    def setUp(self):
        self.service = WeiboCaptureService('http://weibo.com/')

    def test_capture_to_file(self):
        file_path = '/tmp/weibo_capture.png'
        self.service.capture_to_file(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_get_relative_url_by_base64_media_path(self):
        tmp_name = '.gitignore'
        base64_media_path = base64.b64encode(tmp_name)
        self.assertEqual('/media/' + tmp_name, self.service.get_media_relative_path_by(base64_media_path))

    def test_get_relative_url_not_exists(self):
        tmp_name = 'notexists_file'
        base64_media_path = base64.b64encode(tmp_name)
        self.assertEqual(static(settings.DEFAULT_WEIBO_CAPTURE_IMAGE),
                         self.service.get_media_relative_path_by(base64_media_path))
