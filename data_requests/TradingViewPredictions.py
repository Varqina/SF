import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.get("https://www.tradingview.com/")
accept = driver.find_element_by_css_selector("body > div:nth-child(9) > div > div > div > article > div.main-content-mxEBwIhg > div > button > span")
accept.click()
invoke_sign_in = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[3]/button[1]")
invoke_sign_in.click()
sign_in = driver.find_element_by_css_selector("#overlap-manager-root > div > span > div.menu-3T0QrMcJ.menuWrap-g78rwseC > div > div > div.item-2IihgTnv.item-89Fo62DY.item-PoBSqYYZ.withIcon-2IihgTnv.withIcon-89Fo62DY > div.labelRow-2IihgTnv.labelRow-89Fo62DY > div")
sign_in.click()
email = driver.find_element_by_css_selector("#overlap-manager-root > div > div.tv-dialog__modal-wrap.tv-dialog__modal-wrap--contain-size > div > div > div > div > div > div > div:nth-child(1) > div.i-clearfix > div > span > span")
email.click()


