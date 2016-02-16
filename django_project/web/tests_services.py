import base64
import mock
import os
import redis_lock
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from django.conf import settings
from django.templatetags.static import static
from django.test import TestCase
from django_redis import get_redis_connection

from web.exceptions import WeiboNotLoginException
from web.services import WeiboCaptureService, BrowserService
from django_project import utils


@mock.patch('selenium.webdriver.Chrome')
class BrowserServiceTest(TestCase):
    """
    Test for BrowserService
    """
    @mock.patch('selenium.webdriver.Chrome')
    def setUp(self, *args):
        redis_lock.reset_all(get_redis_connection("default"))
        self.service = BrowserService()

    def test_init_chrome_raise_exception(self, mock_chrome):
        mock_chrome.side_effect = [Exception(), mock.Mock()]
        BrowserService()
        self.assertEqual(2, mock_chrome.call_count)

    def test_delete_instance_with_exception(self, *args):
        self.service.screen = None
        self.service.browser = None

        del self.service
        self.assertTrue(True)

    def test_when_delete_instance_relase_lock(self, *args):
        mock_lock = mock.Mock()
        self.service.browser_lock = mock_lock
        del self.service
        mock_lock.release.assert_called_once_with()

    @mock.patch('os.remove')
    def test_when_use_tmp_path_delete_instance_will_remove_folder(self, mock_remove, *args):
        self.service.browser_lock = None
        path = self.service.browser_user_path
        del self.service
        mock_remove.assert_called_once_with(path)

    def test_get(self, *args):
        self.service.browser = mock.Mock()
        self.service.get('abc')
        self.service.browser.get.assert_called_once_with('abc')
        self.service.browser.execute_script.assert_called_once_with(self.service.jquery)

    @mock.patch.object(EC, 'presence_of_element_located', return_value=mock.Mock(return_value='element1'))
    def test_find_element(self, mock_method, *args):
        self.assertEqual('element1', self.service.find_element('abc'))

    @mock.patch.object(EC, 'element_to_be_clickable', return_value=mock.Mock(return_value='element2'))
    def test_find_element_visible_and_clickable(self, mock_method, *args):
        self.assertEqual('element2', self.service.find_element_visible_and_clickable('abc'))

    @mock.patch.object(EC, 'presence_of_all_elements_located', return_value=mock.Mock(return_value='element3'))
    def test_find_elements(self, mock_method, *args):
        self.assertEqual('element3', self.service.find_elements('abc'))

    def test_fill_input(self, *args):
        mock_element = mock.Mock()
        self.service.fill_input(mock_element, 123)
        mock_element.clear.assert_called_once_with()
        mock_element.send_keys.assert_called_once_with(123)

    def test_select_checkbox_from_uncheck_to_check(self, *args):
        mock_element = mock.Mock()
        mock_element.is_selected.return_value = False
        self.service.select_checkbox(mock_element)
        mock_element.click.assert_called_once_with()

    def test_select_checkbox_from_check_to_uncheck(self, *args):
        mock_element = mock.Mock()
        mock_element.is_selected.return_value = True
        self.service.select_checkbox(mock_element, value=False)
        mock_element.click.assert_called_once_with()

    def test_execute_script(self, *args):
        self.service.browser = mock.Mock()
        self.service.execute_script('abc')
        self.service.browser.execute_script.assert_called_once_with('abc')


@mock.patch('selenium.webdriver.Chrome')
class WeiboCaptureServiceTest(TestCase):
    """
    Test for WeiboCaptureService
    """
    @mock.patch('selenium.webdriver.Chrome')
    def setUp(self, *args):
        redis_lock.reset_all(get_redis_connection("default"))
        self.service = WeiboCaptureService('http://weibo.com/')

    @mock.patch.object(WeiboCaptureService, 'auto_login')
    def test_initial_auto_login_called(self, mock_auto_login, *args):
        WeiboCaptureService(None, auto_login=True)
        mock_auto_login.assert_called_once_with()

    def test_auto_login_when_got_cookie(self, *args):
        self.service.browser = mock.Mock(current_url=self.service.login_success_feature_url)
        self.service.get = mock.Mock()
        self.service.auto_login()
        self.service.get.assert_called_once_with(self.service.login_success_feature_url)
        self.assertTrue(self.service.login_success)

    def test_auto_login_when_no_cookie(self, *args):
        self.service.browser = mock.Mock(current_url='abc')
        self.service.get = mock.Mock()
        self.service.do_login = mock.Mock()
        self.service.auto_login()
        self.service.get.assert_called_once_with(self.service.login_success_feature_url)
        self.service.do_login.assert_called_once_with()

    @mock.patch.object(WeiboCaptureService, 'get')
    @mock.patch.object(WeiboCaptureService, 'find_element_visible_and_clickable')
    @mock.patch.object(WeiboCaptureService, 'select_checkbox')
    @mock.patch.object(WeiboCaptureService, 'fill_input')
    @mock.patch.object(WeiboCaptureService, 'find_element',
                       return_value=mock.Mock(is_displayed=mock.Mock(return_value=False)))
    def test_do_login(self, *args):
        self.service.browser = mock.Mock(current_url=settings.SINA_WEIBO_LOGIN_REDIRECT_PAGE)
        self.service.do_login()
        self.assertTrue(self.service.login_success)

    @mock.patch.object(WeiboCaptureService, 'get')
    @mock.patch.object(WeiboCaptureService, 'find_element_visible_and_clickable')
    @mock.patch.object(WeiboCaptureService, 'select_checkbox')
    @mock.patch.object(WeiboCaptureService, 'fill_input')
    @mock.patch.object(WeiboCaptureService, 'find_element',
                       return_value=mock.Mock(is_displayed=mock.Mock(return_value=False)))
    @mock.patch.object(utils, 'generate_user_media_image_path')
    def test_do_login_failed(self, mock_method, *args):
        mock_method.return_value = 'a_path'
        file_path = os.path.join(settings.MEDIA_ROOT, 'a_path')
        self.service.browser = mock.Mock(current_url='abc')
        self.service.do_login()
        self.service.browser.save_screenshot.assert_called_once_with(file_path)
        self.assertFalse(self.service.login_success)

    @mock.patch.object(Image, 'open')
    def test_capture_to_file_when_login_success(self, mock_open, *args):
        file_path = '/tmp/weibo_capture.png'
        self.service.login_success = True
        self.service.get = mock.Mock()
        self.service.browser = mock.Mock()
        self.service.browser.find_element_by_css_selector.side_effect = NoSuchElementException()
        self.service.find_element_visible_and_clickable = mock.Mock()
        self.service.capture_to_file(file_path)
        self.service.get.assert_called_once_with(self.service.url)
        self.service.browser.save_screenshot.assert_called_once_with(file_path)

    def test_capture_to_file_not_login_raise_exception(self, *args):
        self.assertRaises(WeiboNotLoginException, self.service.capture_to_file, 'abc')

    @mock.patch.object(Image, 'open')
    @mock.patch.object(utils, 'crop_image')
    def test_capture_document_info_to_file(self, mock_crop_image, mock_open, *args):
        file_path = '/tmp/weibo_capture.png'
        self.service.login_success = True
        self.service._fetch_url = mock.Mock()
        self.service.find_element_visible_and_clickable = mock.Mock()
        self.service.find_element = mock.Mock(return_value=mock.Mock(
            location={'x':4, 'y':5},
            size={'width':3, 'height':4}
        ))
        self.service.execute_script = mock.Mock()
        self.service.capture_feed_to_file(file_path)
        mock_crop_image.assert_called_once_with(file_path, 1, 2, 9, 10)

    def test_get_relative_url_by_base64_media_path(self, *args):
        tmp_name = '.gitignore'
        base64_media_path = base64.b64encode(tmp_name)
        self.assertEqual('/media/' + tmp_name, self.service.get_media_relative_path_by(base64_media_path))

    def test_get_relative_url_not_exists(self, *args):
        tmp_name = 'notexists_file'
        base64_media_path = base64.b64encode(tmp_name)
        self.assertEqual(static(settings.DEFAULT_WEIBO_CAPTURE_IMAGE),
                         self.service.get_media_relative_path_by(base64_media_path))
