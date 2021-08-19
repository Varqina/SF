import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import Password.PasswordStrings as list_of_strings

class TradingViewPredictions:
    def __init__(self):
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.implicitly_wait(10)
        self.driver.get("https://www.tradingview.com/")
        time.sleep(2)
        accept = self.driver.find_element_by_css_selector("body > div:nth-child(9) > div > div > div > article > div.main-content-mxEBwIhg > div > button > span")
        accept.click()
        invoke_sign_in = self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[3]/button[1]")
        invoke_sign_in.click()
        sign_in = self.driver.find_element_by_css_selector("#overlap-manager-root > div > span > div.menu-3T0QrMcJ.menuWrap-g78rwseC > div > div > div.item-2IihgTnv.item-89Fo62DY.item-PoBSqYYZ.withIcon-2IihgTnv.withIcon-89Fo62DY > div.labelRow-2IihgTnv.labelRow-89Fo62DY > div")
        sign_in.click()
        email = self.driver.find_element_by_css_selector("#overlap-manager-root > div > div.tv-dialog__modal-wrap.tv-dialog__modal-wrap--contain-size > div > div > div > div > div > div > div:nth-child(1) > div.i-clearfix > div > span > span")
        email.click()
        username_login = self.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[1]/div[1]/input')
        username_login.send_keys(list_of_strings.email)
        user_password_login = self.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[2]/div[1]/input')
        user_password_login.send_keys(list_of_strings.trading_view_password)
        sign_in_button = self.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div/div/div/div/div/div/form/div[5]/div[2]/button')
        sign_in_button.click()