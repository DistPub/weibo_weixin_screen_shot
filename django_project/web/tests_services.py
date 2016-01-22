import os

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
        if os.path.exists(file_path):
            os.remove(file_path)
        self.service.capture_to_file(file_path)
        self.assertTrue(os.path.exists(file_path))
