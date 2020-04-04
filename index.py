from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
driver.get('http://leetcode.com/')

#Find element to sign in
sign_in_button = driver.find_element_by_link_text('Sign in')
sign_in_button.click()

#Enter credentials
username_dialog = driver.find_element_by_name('login')
password_dialog = driver.find_element_by_name('password')

username_dialog.send_keys('andygautam4ever@gmail.com')
password_dialog.send_keys('gautamzhang5ever')

wait = WebDriverWait(driver, 5)
login_button = wait.until(EC.element_to_be_clickable((By.ID, 'signin_btn')))
login_button.click()