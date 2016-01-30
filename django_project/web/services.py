import base64
from time import sleep

import os
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.templatetags.static import static
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from django_project import utils
from web.exceptions import WeiboNotLoginException

logger = logging.getLogger()


class BrowserService(object):
    """
    Browser Service
    """
    def __init__(self):
        """
        Init BaseBrowserService
        """
        display = Display(visible=0, size=(1920, 1200))
        display.start()
        self.screen = display

        self.browser_lock, self.browser_user_path = utils.get_chrome_resource()
        logger.info('BrowserService.__init__ lock:%s, path:%s' % (self.browser_lock, self.browser_user_path))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-data-dir=' + self.browser_user_path)
        chrome_options.add_argument('homepage=' + settings.CHROME_HOME_PAGE)
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
        except Exception as e:
            logger.error('BrowserService.__init__ driver error:' + str(e))
            driver = webdriver.Chrome()
        driver.set_window_size(1920, 1200)
        self.browser = driver
        self.wait = WebDriverWait(self.browser, 60)
        self.jquery = open(settings.JQUERY_JS_FILE).read()

    def __del__(self):
        """
        Before delete instance, let's close display and driver
        """
        try:
            self.screen.stop()
        except Exception as e:
            logger.warning('BrowserService.__del__ stop screen exception:' + str(e))

        try:
            if self.browser_lock:
                self.browser_lock.release()
            else:
                os.remove(self.browser_user_path)
        except Exception as e:
            logger.warning('BrowserService.__del__ release lock or remove tmp folder exception:' + str(e))

        try:
            self.browser.quit()
        except Exception as e:
            logger.warning('BrowserService.__del__ quit browser exception:' + str(e))

    def get(self, url):
        """
        Shortcut to get resource and load jquery
        """
        self.browser.get(url)
        self.browser.execute_script(self.jquery)

    def find_element(self, selector):
        """
        Shortcut find element
        """
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def find_element_visible_and_clickable(self, selector):
        """
        Shortcut find element that element is visible and clickable
        """
        return self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))

    def find_elements(self, selector):
        """
        Shortcut find elements
        """
        return self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

    def fill_input(self, web_element, value=None):
        """
        Fill input element
        """
        web_element.clear()
        if value:
            web_element.send_keys(value)

    def select_checkbox(self, web_element, value=True):
        """
        Select checkbox
        """
        if (value and not web_element.is_selected()) or (not value and web_element.is_selected()):
            web_element.click()

    def execute_script(self, script):
        """
        Shortcut to execute script
        """
        return self.browser.execute_script(script)


class WeiboCaptureService(BrowserService):
    """
    Weibo capture sevice
    """
    document_detail_page_comment_class = 'span[node-type="comment_btn_text"]'
    login_success_feature_url = 'http://account.weibo.com/set/index'
    login_page_url = 'http://weibo.com/login.php'

    def __init__(self, url, auto_login=False):
        """
        Init service
        :param url: weibo url
        """
        super(WeiboCaptureService, self).__init__()
        self.url = url
        self.login_success = False

        # check login status
        if auto_login:
            self.auto_login()

    def auto_login(self):
        """
        Keep weibo login status

        First we check currect cookie login status by get a featured url, that url only access when user login-ed.
        If failed then we go to weibo login page do login.
        """
        self.get(self.login_success_feature_url)
        if self.browser.current_url == self.login_success_feature_url:
            self.login_success = True
        else:
            self.login_success = False
            self.do_login()

    def do_login(self):
        """
        Go to weibo login page input username and password to login.
        """
        username_selector = '#pl_login_form input[name="username"]'
        password_selector = '#pl_login_form input[name="password"]'
        remember_password_selector = '#login_form_savestate'
        submit_selecotr = '#pl_login_form .login_btn a'
        account_login_type_selector = 'a[node-type="normal_tab"]'

        self.get(self.login_page_url)

        # make form visible
        username_input = self.find_element(username_selector)
        if not username_input.is_displayed():
            self.find_element_visible_and_clickable(account_login_type_selector).click()
        self.find_element_visible_and_clickable(username_selector)

        self.fill_input(username_input, settings.SINA_WEIBO_USERNAME)
        self.fill_input(self.find_element(password_selector), settings.SINA_WEIBO_PASSWORD)
        self.select_checkbox(self.find_element(remember_password_selector))
        self.find_element_visible_and_clickable(submit_selecotr).click()

        # wait for iframe do login complete
        # TODO: need make a better way to check login response returned
        sleep(3)

        if self.browser.current_url.startswith(settings.SINA_WEIBO_LOGIN_REDIRECT_PAGE):
            self.login_success = True
        else:
            file_path = utils.generate_user_media_image_path(prefix='error')
            self.browser.save_screenshot(file_path)
            logger.error('WeiboCaptureService.do_login failed, please check screen shot file:' + file_path)

    def capture_to_file(self, file_path):
        """
        Capture weibo url specified page to a file
        """
        if not self.login_success:
            raise WeiboNotLoginException()

        self.get(self.url)
        self.find_element_visible_and_clickable(self.document_detail_page_comment_class)
        self.browser.save_screenshot(file_path)

    @staticmethod
    def get_media_relative_path_by(base64_media_path, default=settings.DEFAULT_WEIBO_CAPTURE_IMAGE):
        """
        Return media relative path
        If file not exists, will return default file
        """
        user_media_path = base64.b64decode(base64_media_path)

        if os.path.exists(os.path.join(settings.MEDIA_ROOT, user_media_path)):
            return reverse('media', kwargs={'path': user_media_path})
        else:
            return static(default)
