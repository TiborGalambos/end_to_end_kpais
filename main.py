import time
from time import sleep

import selenium
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
import re
from datetime import datetime


import credentials

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select




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
    side_bar = wait.until((presence_of_element_located((By.XPATH, '//li[@data-testid="kind-group"]'))))
    users = side_bar.find_element(By.XPATH, '//*[text()="Users"]')
    wait.until(EC.element_to_be_clickable(users))
    users.click()

    # 4.
    user = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'TiborGalambos')))
    user.click()

    # 5.
    nav_tab = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'UnderlineNav-body')))
    repositories = nav_tab.find_element(By.XPATH, '//*[@data-tab-item="repositories"]')
    repositories.click()

    # 6.
    language_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'language-options')))
    language_dropdown.click()

    assert "Python" in language_dropdown.text, "Python not present in dropdown"

    # 7.
    python_lang = language_dropdown.find_element(By.XPATH, '//*[text()="Python"]')
    python_lang.click()

    # 8.
    repository_list = wait.until(presence_of_element_located((By.ID, 'user-repositories-list')))
    repository = wait.until(EC.element_to_be_clickable((repository_list.find_element(By.XPATH, '//a[@href="/TiborGalambos/freebase-person-parser" and @itemprop="name codeRepository"]'))))
    repository.click()

    # 9.
    commits = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="Commits on main"]')))
    commits.click()

    body = wait.until(presence_of_element_located((By.TAG_NAME, 'body')))
    assert 'dddcbfe' in body.text, 'commit number not found'

    # 10.
    commit = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'dddcbfe')))
    commit.click()

    # 11.
    three_dots = wait.until(presence_of_element_located((By.CLASS_NAME, 'file-actions')))
    three_dots.click()

    # 12.
    dropdown_menu = wait.until(presence_of_element_located((By.TAG_NAME, 'details-menu')))
    view_file = dropdown_menu.find_element(By.XPATH,
                                           "//a[@data-ga-click='View file, click, location:files_changed_dropdown']")
    view_file.click()

    # 13.
    raw = wait.until(presence_of_element_located((By.XPATH, "//a[@data-testid='raw-button']")))
    raw.click()

    code = wait.until(presence_of_element_located((By.TAG_NAME, 'pre')))
    assert 'import re' in code.text and 'Tibor Galambos' not in code.text, 'raw file did not open'


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
    body = wait.until(presence_of_element_located((By.TAG_NAME, 'body')))
    assert 'Account and profile documentation' in body.text, 'documentation not found'

    body.send_keys(Keys.END)

    # 4.
    radio_button = wait.until(presence_of_element_located((By.XPATH, '//label[@for="survey-yes"]')))
    wait.until(EC.element_to_be_clickable(radio_button))
    radio_button_image = radio_button.find_element(By.TAG_NAME, 'svg')
    wait.until(EC.element_to_be_clickable(radio_button_image))
    radio_button_image.click()

    # 5.
    submit = wait.until(presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
    submit.click()

    feedback_message = wait.until(presence_of_element_located((By.XPATH, '//p[@data-testid="survey-end"]')))
    assert 'Thank you! We received your feedback.' in feedback_message.text, 'thank you message not displayed'

def test_dsl_speed():
    wait = WebDriverWait(driver, 5)
    driver.set_window_size(1920, 1080)
    driver.get('https://www.dsl.sk')

    title_bar = wait.until(presence_of_element_located((By.XPATH, '//div[@id="title_bar"]')))

    assert 'neprihlásený' in title_bar.text, 'user should not be logged in'

    # 1
    login_button_in_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/user.php?action=login"]')))
    login_button_in_header.click()

    # 2.
    login_form = wait.until(presence_of_element_located((By.XPATH, '//form[@action="user.php" and @method="post"]')))
    username = login_form.find_element(By.NAME, 'login')
    username.send_keys(credentials.username)
    password = login_form.find_element(By.NAME, 'password')
    password.send_keys('wrong password' + Keys.ENTER)

    login_form = wait.until(presence_of_element_located((By.XPATH, '//form[@action="user.php" and @method="post"]')))
    assert 'Nesprávne meno alebo heslo' in login_form.text, 'user logged in with wrong credentials'

    # 3.
    login_form = wait.until(presence_of_element_located((By.XPATH, '//form[@action="user.php" and @method="post"]')))
    username = login_form.find_element(By.NAME, 'login')
    username.send_keys(credentials.username)
    password = login_form.find_element(By.NAME, 'password')
    password.send_keys(credentials.password + Keys.ENTER)

    title_bar = wait.until(presence_of_element_located((By.XPATH, '//div[@id="title_bar"]')))
    assert 'prihlásený' in title_bar.text, 'user should be logged in with correct credentials'

    # 4.
    speedmeter = wait.until(presence_of_element_located((By.LINK_TEXT, 'Speedmeter')))
    speedmeter.click()

    # 5.
    speedmeter_start = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="speedmeter.php?id=speed_test"]')))
    speedmeter_start.click()

    body = wait.until(presence_of_element_located((By.XPATH, '//div[@id="body"]')))

    pattern = 'alebo tiež (\d+\.\d+) KB/sec'
    connection_speed = re.search(pattern, body.text)

    # 6.
    results_table = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="speedmeter_history.php"]')))
    results_table.click()

    body = wait.until(presence_of_element_located((By.XPATH, '//div[@id="body"]')))
    table = body.find_element(By.TAG_NAME, 'table')
    results_table = table.find_element(By.XPATH, '//table/tbody/tr')

    pattern = r'Vaše posledné merania:\n\n.+\s(\d+\.\d+)\sKB/sec'
    first_result = re.search(pattern, results_table.text)
    assert str(connection_speed.group(1)) == str(first_result.group(1)), 'connection not found'

    driver.back()

    # 7.
    try:
        form = wait.until(presence_of_element_located((By.XPATH, '//form[@action="speedmeter.php" and @method="post"]')))
        type_form = form.find_element(By.NAME, 'type')
        select = Select(type_form)
        select.select_by_value('OTHER')
        provider = form.find_element(By.NAME, 'provider')
        select = Select(provider)
        select.select_by_value('OTHER')
        other_provider = form.find_element(By.NAME, 'other_provider')
        other_provider.send_keys('test' + Keys.ENTER)
    except TimeoutException:
        assert False, 'form not found'

    body_text = wait.until(presence_of_element_located((By.XPATH, '//div[@id="body"]')))
    assert 'Ďakujeme za odoslanie parametrov' in body_text.text

    # 8.
    logout_button_in_header = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/user.php?action=logout"]')))
    logout_button_in_header.click()

    title_bar = wait.until(presence_of_element_located((By.XPATH, '//div[@id="title_bar"]')))
    assert 'neprihlásený' in title_bar.text, 'user should not be logged in'


def test_dsl_required_fields():
    wait = WebDriverWait(driver, 5)
    driver.set_window_size(1920, 1080)
    driver.get('https://www.dsl.sk')

    # 1.
    searchbox = wait.until(presence_of_element_located((By.NAME, "keyword")))
    searchbox.send_keys('RAM' + Keys.ENTER)

    # 2.
    article = wait.until(
        presence_of_element_located((By.XPATH, '//a[text()="Ceny RAM aj flash sa majú už otočiť a začať rásť"]')))
    article.click()

    # 3.
    comment = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Pridať komentár"]')))
    comment.click()

    # 4.
    textarea = wait.until(presence_of_element_located((By.NAME, 'msg')))
    textarea.send_keys('Lorem ipsum')

    # 6.
    submit_button = wait.until(presence_of_element_located((By.XPATH, '//input[@value="Pridať"]')))
    submit_button.click()

    body = wait.until(presence_of_element_located((By.NAME, 'add_form')))
    assert 'Meno musí mať dĺžku aspoň 3 znaky.' in body.text

    # 7.
    author = wait.until(presence_of_element_located((By.NAME, 'author')))
    author.send_keys(credentials.username)

    textarea = wait.until(presence_of_element_located((By.NAME, 'msg')))
    textarea.clear()

    # 8.
    submit_button = wait.until(presence_of_element_located((By.XPATH, '//input[@value="Pridať"]')))
    submit_button.click()

    body = wait.until(presence_of_element_located((By.NAME, 'add_form')))
    assert 'Meno je už zaregistrované' in body.text

    current_time = datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # 10.
    author = wait.until(presence_of_element_located((By.NAME, 'author')))
    author.clear()
    author.send_keys(time_string)

    title = wait.until(presence_of_element_located((By.NAME, 'msg_title')))
    title.send_keys('1234')

    # 11.
    submit_button = wait.until(presence_of_element_located((By.XPATH, '//input[@value="Pridať"]')))
    submit_button.click()

    body = wait.until(presence_of_element_located((By.NAME, 'add_form')))
    assert 'Titulok príspevku musí mať dĺžku aspoň 5 znakov.' in body.text



def run_tests():
    test_results = []

    try:
        test_github_raw_file()
        test_results.append("test_github_raw_file: PASSED")
    except Exception as e:
        test_results.append("test_github_raw_file: FAILED - " + str(e))

    try:
        test_github_send_feedback()
        test_results.append("test_github_send_feedback: PASSED")
    except Exception as e:
        test_results.append("test_github_send_feedback: FAILED - " + str(e))

    try:
        test_dsl_speed()
        test_results.append("test_dsl_speed: PASSED")
    except Exception as e:
        test_results.append("test_dsl_speed: FAILED - " + str(e))

    try:
        test_dsl_required_fields()
        test_results.append("test_dsl_required_fields: PASSED")
    except Exception as e:
        test_results.append("test_dsl_required_fields: FAILED - " + str(e))

    for result in test_results:
        print(result)

if __name__ == "__main__":
    with webdriver.Chrome() as driver:
        run_tests()

# with webdriver.Chrome() as driver:
#
#     test_github_raw_file()
#     test_github_send_feedback()
#     test_dsl_speed()
#     test_dsl_name_required_fields()
