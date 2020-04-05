from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
import time

def get_question_dictionary_of_user(name, driver):
    q_list = driver.find_element_by_xpath("//span[@title='{0}']/parent::a".format(name))
    q_list.click()
    q_dict = {}
    question_person_list = driver.find_elements_by_class_name('question-title')
    for x in range(1, len(question_person_list) + 1):
        question = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[2]/li[{0}]/div/a'.format(x))
        q_dict[question.get_attribute('innerHTML')] = question.get_attribute('href')
    return q_dict

def main():
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

    #Use Nav 
    element = wait.until(EC.invisibility_of_element_located((By.ID, 'signin_btn')))
    problems_nav_button = driver.find_element_by_link_text('Problems')
    problems_nav_button.click()

    #Grab total questions
    total_question_element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/span/span[1]/span")))
    total_questions_completed = total_question_element.get_attribute("innerHTML").split('/')[0]
    print(total_questions_completed)

    #List
    profile = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/ul[2]/li[3]/span/span')
    profile.click()

    profile_lists = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/ul[2]/li[3]/span/ul/div[2]/li[2]/div/div[2]')
    profile_lists.click()

    #Favorite List
    fav_list = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div[1]/div/div/div/div[2]/a[1]')))
    fav_list.click()

    fav_question_dict = {}
    question_fav_list = driver.find_elements_by_class_name('question-title')
    for x in range(1, len(question_fav_list) + 1):
        question = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[2]/li[{0}]/div/a'.format(x))
        fav_question_dict[question.get_attribute('innerHTML')] = question.get_attribute('href')

    names_list = ["Andy", "Gautam"]
    Andy_dict = get_question_dictionary_of_user('Andy', driver)
    Gautam_dict = get_question_dictionary_of_user('Gautam', driver)

    common_dict = {}
    for val in Andy_dict:
        if val in Gautam_dict:
            common_dict[val] = Gautam_dict[val]

    if(len(common_dict) == len(fav_question_dict)):
        driver.quit()
    else:
        print(len(common_dict))
        print(len(fav_question_dict))
        for x in common_dict:
            if x not in fav_question_dict:
                driver.get(common_dict.get(x))
                fav_q_btn = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Add to List']/parent::button")))
                fav_q_btn.click()
                time.sleep(0.5)
                fav_q_btn.click()

if __name__ == "__main__":
    main()
    