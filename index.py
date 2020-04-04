from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json

with open('credentials.json') as data_file:
    data = json.load(data_file)

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

username_dialog.send_keys(data['username'])
password_dialog.send_keys(data['password'])

wait = WebDriverWait(driver, 10)
element = wait.until(EC.invisibility_of_element_located((By.ID, 'initial-loading')))
login_button = wait.until(EC.element_to_be_clickable((By.ID, 'signin_btn')))
login_button.click()