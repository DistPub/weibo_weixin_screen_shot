# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display


def main():
    display = Display(visible=0, size=(1920, 1200))
    display.start()

    driver = webdriver.Chrome()
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1200)
    wait = WebDriverWait(driver, 60)

    url = 'http://weibo.com/lovemyliwu'

    driver.get(url)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'WB_feed_type')))
    driver.save_screenshot('/tmp/weibo.png')

    driver.close()
    display.stop()


if __name__ == '__main__':
    main()
