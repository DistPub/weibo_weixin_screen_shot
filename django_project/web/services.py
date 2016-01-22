from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

        driver = webdriver.Chrome()
        driver.set_window_size(1920, 1200)
        self.browser = driver

    def __del__(self):
        """
        Before delete instance, let's close display and driver
        """
        self.browser.close()
        self.screen.stop()


class WeiboCaptureService(BrowserService):
    """
    Weibo capture sevice
    """
    weibo_page_feature_class = 'WB_feed_type'

    def __init__(self, url):
        """
        Init service
        :param url: weibo url
        """
        self.url = url
        super(WeiboCaptureService, self).__init__()

    def capture_to_file(self, file_path):
        """
        Capture weibo url specified page to a file
        """
        wait = WebDriverWait(self.browser, 60)
        self.browser.get(self.url)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, self.weibo_page_feature_class)))
        self.browser.save_screenshot(file_path)
