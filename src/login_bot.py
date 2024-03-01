from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *

from bs4 import BeautifulSoup
import json
import time

from . import settings


class BaseLogin(object):
    def __init__(self, phonenumber, first_name, last_name, profile_path, base_dir):
        self.phonenumber = phonenumber
        self.first_name = first_name
        self.last_name = last_name
        self.profile_path = profile_path
        self.base_dir = base_dir

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument(f'--user-data-dir={self.base_dir}')

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.long_wait = WebDriverWait(self.driver, 60 * 5)
        self.short_wait = WebDriverWait(self.driver, 500)

        self.javascript_click = "arguments[0].click();"
        self.javascript_localstorage = 'return JSON.stringify(localStorage);'

    def go_to_site(self, url):
        while True:
            try:
                self.driver.get(url)
                break
            except WebDriverException:
                print("check your internet connection or turn of your proxy!")
                time.sleep(10)

    def insert_phonenumber(self):
        pass

    def insert_name(self):
        pass

    def element_clickable(self, data, selector_type='cls'):
        # Wait until an element becomes stale (indicating page change)
        if selector_type == 'cls':
            return self.short_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, data)))
        elif selector_type == 'css':
            return self.short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, data)))
        elif selector_type == 'xpath':
            return self.short_wait.until(EC.element_to_be_clickable((By.XPATH, data)))
        else:
            return self.short_wait.until(EC.element_to_be_clickable((By.ID, data)))

    def wait_for_update(self, data, selector_type='cls'):
        # Wait until an element becomes stale (indicating page change)
        if selector_type == 'cls':
            self.long_wait.until(EC.presence_of_element_located((By.CLASS_NAME, data)))
        elif selector_type == 'css':
            self.long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, data)))
        elif selector_type == 'xpath':
            self.long_wait.until(EC.presence_of_element_located((By.XPATH, data)))
        else:
            self.long_wait.until(EC.presence_of_element_located((By.ID, data)))

    def click_anyway(self, selector, select_type='xpath'):
        while True:
            try:
                if select_type == 'xpath':
                    self.driver.find_element(By.XPATH, selector).click()
                elif select_type == 'id':
                    self.driver.find_element(By.ID, selector).click()
                elif select_type == 'cls':
                    self.driver.find_element(By.CLASS_NAME, selector).click()
                else:
                    self.driver.find_element(By.CSS_SELECTOR, selector).click()
                break
            except ElementClickInterceptedException:
                continue

    @staticmethod
    def clear_anyway(element: WebElement):
        while True:
            try:
                element.clear()
                break
            except InvalidElementStateException:
                continue

    def close_browser(self):
        self.driver.quit()


# TODO: rewrite this
class EitaaLogin(BaseLogin):
    def __init__(self, phonenumber, first_name, last_name, profile_path, base_dir):
        super(EitaaLogin, self).__init__(phonenumber, first_name, last_name, profile_path, base_dir)

        self.go_to_site(settings.LOGIN_EITAA)

    def main(self):
        self.wait_for_update('input-field-input')
        self.insert_phonenumber()
        self.wait_for_update('avatar-edit-canvas')
        self.name_input(self.first_name, self.last_name)

        menu_xpath = '//*[@id="column-left"]/div/div/div[1]/div[1]/div[2]/div[1]'
        self.wait_for_update(menu_xpath, 'xpath')
        self.set_profile(self.profile_path)

        waiting_for_save_data = '/html/body/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]'
        self.wait_for_update(waiting_for_save_data, 'xpath')
        self.close_browser()

    def insert_phonenumber(self):
        insert_num_xpath = '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]'
        insert_element = self.driver.find_element(By.XPATH, insert_num_xpath)
        insert_element.clear()
        insert_element.send_keys(self.phonenumber)
        btn_cls_name = '.btn-primary'
        btn_click = self.driver.find_element(By.CSS_SELECTOR, btn_cls_name)
        btn_click.click()

    def name_input(self, fname, lname):
        fname_xpath = '/html/body/div[1]/div/div[2]/div[5]/div/div[2]/div[1]/div[1]'
        lname_xpath = '/html/body/div[1]/div/div[2]/div[5]/div/div[2]/div[2]/div[1]'

        fname_element = self.driver.find_element(By.XPATH, fname_xpath)
        lname_element = self.driver.find_element(By.XPATH, lname_xpath)

        fname_element.send_keys(fname)
        lname_element.send_keys(lname)

        btn_xpath = '/html/body/div[1]/div/div[2]/div[5]/div/div[2]/button'
        btn_element = self.driver.find_element(By.XPATH, btn_xpath)

        btn_element.click()

    def set_profile(self, profile_path):
        settings_xpath = '/html/body/div[2]/div[1]/div[1]/div/div/div[1]/div[1]/div[2]/div[3]/div[3]/div'
        menu_xpath = '//*[@id="column-left"]/div/div/div[1]/div[1]/div[2]/div[1]'
        pencil_xpath = '//*[@id="column-left"]/div/div[2]/div[1]/button[2]'
        avatar_xpath = '//*[@id="column-left"]/div/div[3]/div[2]/div/div[1]/avatar-element'
        menu_element = self.driver.find_element(By.XPATH, menu_xpath)
        menu_element.click()
        self.wait_for_update(settings_xpath, 'xpath')

        settings_element = self.driver.find_element(By.XPATH, settings_xpath)
        settings_element.click()

        self.wait_for_update(pencil_xpath, 'xpath')

        pencil_element = self.element_clickable(pencil_xpath, 'xpath')
        pencil_element.click()

        self.wait_for_update(avatar_xpath, 'xpath')

        file_input = self.driver.find_element(By.CLASS_NAME, 'avatar-photo')
        file_input.send_keys(profile_path)

        confirm_image_btn_xpath = '/html/body/div[5]/div/button'
        self.wait_for_update(confirm_image_btn_xpath, 'xpath')

        confirm_btn_xpath = '//*[@id="column-left"]/div/div[3]/div[2]/button'
        self.wait_for_update(confirm_btn_xpath, 'xpath')
        confirm_element = self.driver.find_element(By.XPATH, confirm_btn_xpath)
        confirm_element.click()


class RubikaLogin(BaseLogin):
    def __init__(self, phonenumber, first_name, last_name, profile_path, base_dir):
        super(RubikaLogin, self).__init__(phonenumber, first_name, last_name, profile_path, base_dir)

        self.go_to_site(settings.LOGIN_RUBIKA)

        self.localstorage = dict()

    def main(self):
        input_xpath = '//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/div[3]/input[1]'
        self.wait_for_update(input_xpath, 'xpath')
        self.insert_phonenumber()
        self.element_clickable('//*[@id="chats"]/rb-chats/div[1]/div[1]/div[2]/div', 'xpath')
        self.set_name(self.first_name, self.last_name, self.profile_path)

        self.localstorage = json.loads(self.driver.execute_script(self.javascript_localstorage))
        self.close_browser()
        return self.localstorage

    def insert_phonenumber(self):
        input_xpath = '//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/div[3]/input[1]'
        btn_xpath = '//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/button/div'

        insert_element = self.driver.find_element(By.XPATH, input_xpath)
        btn_element = self.driver.find_element(By.XPATH, btn_xpath)

        insert_element.send_keys(self.phonenumber)
        btn_element.click()

    def set_name(self, fname, lname, profile_path):

        menu_xpath = '//*[@id="chats"]/rb-chats/div[1]/div[1]/div[2]/div'

        menu_element = self.driver.find_element(By.XPATH, menu_xpath)
        menu_element.click()

        setting_xpath = '/html/body/div[2]/div[3]/div'
        setting_element = self.element_clickable(setting_xpath, 'xpath')
        setting_element.click()

        edit_xpath = '//*[@id="1000"]/app-setting-modal/div[2]/div/div/div[3]/div/div/div/button[1]/div'
        edit_element = self.element_clickable(edit_xpath, 'xpath')

        self.driver.execute_script(self.javascript_click, edit_element)

        input_fname_xpath = ('/html/body/app-root/div/div/div[1]/sidebar-container/div/sidebar-view['
                             '1]/div/modal-profile-edit/div[2]/div/div[1]/div/div/form/div[1]/input')
        input_lname_xpath = ('/html/body/app-root/div/div/div[1]/sidebar-container/div/sidebar-view['
                             '1]/div/modal-profile-edit/div[2]/div/div[1]/div/div/form/div[2]/input')

        input_fname_element = self.element_clickable(input_fname_xpath, 'xpath')
        input_lname_element = self.driver.find_element(By.XPATH, input_lname_xpath)
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        while True:
            try:
                input_fname_element.clear()
                break
            except InvalidElementStateException:
                continue
        input_fname_element.send_keys(fname)

        input_lname_element.clear()
        input_lname_element.send_keys(lname)

        file_input.send_keys(profile_path)

        ok_btn_xpath = '//*[@id="modal-avatar-resize"]/div/modal-avatar-resize/button/div/div'
        ok_btn = self.element_clickable(ok_btn_xpath, 'xpath')
        self.driver.execute_script(self.javascript_click, ok_btn)

        final_btn_xpath = '//*[@id="modal-profile-edit"]/modal-profile-edit/div[2]/button/div/div'
        final_btn = self.element_clickable(final_btn_xpath, 'xpath')
        self.driver.execute_script(self.javascript_click, final_btn)
        self.wait_for_update(edit_xpath, 'xpath')


class SoroushLogin(BaseLogin):
    def __init__(self, phonenumber, first_name, last_name, profile_path, base_dir):
        super(SoroushLogin, self).__init__(phonenumber, first_name, last_name, profile_path, base_dir)

        self.confirm_number_btn_params = {'class': 'Button default primary has-ripple'}
        self.go_to_site(settings.LOGIN_SOROUSH)

    def main(self):
        self.wait_for_update('sign-in-phone-number', 'id')
        self.insert_phonenumber()
        self.wait_for_update('registration-first-name', 'id')
        self.name_input(self.first_name, self.last_name, self.profile_path)
        self.wait_for_update('Main', 'id')

        menu_xpath = '//*[@id="LeftMainHeader"]/div[2]/button'
        self.wait_for_update(menu_xpath)

        self.close_browser()

    def insert_phonenumber(self):
        input_id = 'sign-in-phone-number'
        btn_xpath = '/html/body/div[1]/div/div[1]/div/div/div/div/div/form/button'

        insert_element = self.driver.find_element(By.ID, input_id)
        btn_element = self.driver.find_element(By.XPATH, btn_xpath)

        insert_element.clear()
        insert_element.send_keys(self.phonenumber)

        btn_element.click()

    def name_input(self, fname, lname, profile_path):
        fname_id = 'registration-first-name'
        lname_id = 'registration-last-name'
        btn_xpath = '/html/body/div[1]/div/div[1]/div/div/div[2]/div/div/form/button'

        fname_element = self.driver.find_element(By.ID, fname_id)
        lname_element = self.driver.find_element(By.ID, lname_id)
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")

        fname_element.send_keys(fname)
        lname_element.send_keys(lname)
        file_input.send_keys(profile_path)

        # setup profile
        self.wait_for_update('cr-image')
        self.wait_for_update('icon-check')
        profile_btn = self.driver.find_element(By.CLASS_NAME, 'icon-check')
        profile_btn.click()

        # wait for load element
        self.wait_for_update('/html/body/div[1]/div/div[1]/div/div/div[2]/div/div/form/button', 'xpath')
        btn_element = self.driver.find_element(By.XPATH, btn_xpath)

        btn_element.click()

    @staticmethod
    def timer(second):
        time.sleep(second)

    @staticmethod
    def get_btn_status(src, **kwargs):
        soup = BeautifulSoup(src, 'html.parser')
        btn_src = soup.find('button', attrs=kwargs)
        if btn_src is not None:
            return btn_src.text
        return False


# TODO: complete this
class IgapLogin(BaseLogin):
    pass


# TODO: complete this
class BaleLogin(BaseLogin):
    pass
