import time
from time import sleep

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
from selenium.webdriver.support import expected_conditions as EC

def click_link(link_text):
    link = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
    link.click()
    return link

def test_github_raw_file():
    wait = WebDriverWait(driver, 3)
    driver.set_window_size(1920, 1080)
    driver.get('https://github.com/')
    # 1.
    searchbox = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-input')))
    searchbox.click()

    # 2.
    input_field = wait.until(EC.element_to_be_clickable((By.ID, 'query-builder-test')))
    input_field.send_keys('TiborGalambos' + Keys.ENTER)

    # 3.
    users = wait.until(presence_of_element_located((By.LINK_TEXT, 'Users')))
    users.click()

    # 4.
    click_link('TiborGalambos')

    # 5.
    nav_tab = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'UnderlineNav-body')))
    repositories = nav_tab.find_element(By.XPATH, '//*[@data-tab-item="repositories"]')
    repositories.click()

    # 6.
    language_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'language-options')))
    language_dropdown.click()

    # 7.
    python_lang = language_dropdown.find_element(By.XPATH, '//*[text()="Python"]')
    python_lang.click()

    # 8.
    repository_list = wait.until(presence_of_element_located((By.ID, 'user-repositories-list')))
    repository = repository_list.find_element(By.LINK_TEXT, 'freebase-person-parser')
    repository.click()

    # 9.
    # header_box = wait.until(presence_of_element_located((By.CLASS_NAME, 'file-navigation')))
    commits = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="Commits on main"]')))
    commits.click()

    # 10.
    commit = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'dddcbfe')))
    commit.click()

    # 11.
    three_dots = wait.until(presence_of_element_located((By.CLASS_NAME, 'file-actions')))
    three_dots.click()

    # 12.
    dropdown_menu = wait.until(presence_of_element_located((By.TAG_NAME, 'details-menu')))
    view_file = dropdown_menu.find_element(By.XPATH, "//a[@data-ga-click='View file, click, location:files_changed_dropdown']")
    view_file.click()

    # 13.
    raw = wait.until(presence_of_element_located((By.XPATH, "//a[@data-testid='raw-button']")))
    raw.click()

    code = wait.until(presence_of_element_located((By.TAG_NAME, 'pre')))
    print(code.text)
    assert 'import re' in code.text and 'Tibor Galambos' not in code.text


def test_github_send_feedback():
    wait = WebDriverWait(driver, 3)
    driver.set_window_size(1920, 1080)
    driver.get('https://github.com/')
    action = ActionChains(driver)

    # 1.
    product_dropdown = wait.until(presence_of_element_located((By.CLASS_NAME, "HeaderMenu-link")))
    action.move_to_element(product_dropdown).perform()
    documentation_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://docs.github.com']")))
    documentation_link.click()

    # 2.
    new_tab = driver.window_handles[-1]
    driver.switch_to.window(new_tab)
    account_and_profile = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Account and profile')))
    account_and_profile.click()

    # 3.
    body = driver.find_element("tag name", "body")
    body.send_keys(Keys.END)

    # 4.
    radio_button = wait.until(presence_of_element_located((By.XPATH, '//label[@for="survey-yes"]')))
    radio_button = radio_button.find_element(By.TAG_NAME, 'svg')
    radio_button.click()

    # 5.
    submit = wait.until(presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
    submit.click()

    feedback_message = wait.until(presence_of_element_located((By.XPATH, '//p[@data-testid="survey-end"]')))
    print(feedback_message.text)
    assert 'Thank you! We received your feedback.' in feedback_message.text


with webdriver.Chrome() as driver:
    test_github_raw_file()
    test_github_send_feedback()


