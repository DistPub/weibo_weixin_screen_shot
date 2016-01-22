from django.test import TestCase

from web.forms import WeiboCaptureRequestForm


class WeiboCaptureRequestFormTest(TestCase):
    """
    Test for WeiboCaptureRequestForm
    """
    def test_has_text_field(self):
        form = WeiboCaptureRequestForm()
        self.assertIn('url', form.fields.keys())

    def test_error_url_not_valid(self):
        form = WeiboCaptureRequestForm({'url': 'abc'})
        self.assertFalse(form.is_valid())

    def test_correct_url_valid(self):
        form = WeiboCaptureRequestForm({'url': 'http://www.baidu.com'})
        self.assertTrue(form.is_valid())
