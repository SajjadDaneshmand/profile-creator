from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time

from bs4 import BeautifulSoup

from src import settings


class BaseLogin(object):
    def __init__(self, phonenumber):
        self.phonenumber = phonenumber
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 60 * 5)

    def go_to_site(self, url):
        self.driver.get(url)

    def insert_phonenumber(self):
        pass

    def insert_name(self):
        pass

    def wait_for_update(self, data, selector_type='cls'):
        # Wait until an element becomes stale (indicating page change)
        if selector_type == 'cls':
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, data)))
        elif selector_type == 'css':
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, data)))
        elif selector_type == 'xpath':
            self.wait.until(EC.presence_of_element_located((By.XPATH, data)))
        else:
            self.wait.until(EC.presence_of_element_located((By.ID, data)))

    def close_browser(self):
        self.driver.quit()


# TODO: rewrite this
class EitaaLogin(BaseLogin):
    def __init__(self, phonenumber):
        super(EitaaLogin, self).__init__(phonenumber)

        self.go_to_site(settings.LOGIN_EITAA)

    def main(self):
        self.wait_for_update('input-field-input')
        self.insert_phonenumber()
        self.wait_for_update('avatar-edit-canvas')
        self.name_input(settings.FIRST_NAME, settings.LAST_NAME, settings.PICTURE_PATH)

        menu_xpath = '//*[@id="column-left"]/div/div/div[1]/div[1]/div[2]/div[1]'
        self.wait_for_update(menu_xpath, 'xpath')
        self.set_profile(settings.PICTURE_PATH)

        waiting_for_save_data = '/html/body/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]'
        self.wait_for_update(waiting_for_save_data, 'xpath')


        time.sleep(1000)
        self.close_browser()

    def insert_phonenumber(self):
        insert_num_xpath = '/html/body/div[1]/div/div[2]/div[1]/div/div[3]/div[2]/div[1]'
        insert_element = self.driver.find_element(By.XPATH, insert_num_xpath)
        insert_element.clear()
        insert_element.send_keys(self.phonenumber)
        btn_cls_name = '.btn-primary'
        btn_click = self.driver.find_element(By.CSS_SELECTOR, btn_cls_name)
        btn_click.click()

    def name_input(self, fname, lname, profile_path):
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

        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, pencil_xpath)))
        element.click()

        self.wait_for_update(avatar_xpath, 'xpath')

        file_input = self.driver.find_element(By.CLASS_NAME, 'avatar-photo')
        file_input.send_keys(profile_path)

        confirm_image_btn_xpath = '/html/body/div[5]/div/button'
        self.wait_for_update(confirm_image_btn_xpath, 'xpath')

        confirm_btn_xpath = '//*[@id="column-left"]/div/div[3]/div[2]/button'
        self.wait_for_update(confirm_btn_xpath, 'xpath')
        confirm_element = self.driver.find_element(By.XPATH, confirm_btn_xpath)
        confirm_element.click()

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


class RubikaLogin(BaseLogin):
    def __init__(self, phonenumber):
        super(RubikaLogin, self).__init__(phonenumber)

        self.go_to_site(settings.LOGIN_RUBIKA)

    def main(self):
        input_xpath = '//*[@id="auth-pages"]/div/div[2]/div[1]/div/div[3]/div[3]/input[1]'
        self.wait_for_update(input_xpath, 'xpath')
        rubika.insert_phonenumber()
        self.wait_for_update('//*[@id="chats"]/rb-chats/div[1]/div[1]/div[2]/div/div', 'xpath')
        self.set_name(settings.FIRST_NAME, settings.LAST_NAME, settings.PICTURE_PATH)
        print('yesssss')
        time.sleep(6000)
        self.close_browser()

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
        setting_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, setting_xpath)))
        setting_element.click()

        edit_xpath = '//*[@id="1000"]/app-setting-modal/div[2]/div/div/div[3]/div/div/div/button[1]/div'
        self.wait_for_update(edit_xpath, 'xpath')
        print('test')
        edit_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, edit_xpath))) 
        edit_element.click()

        input_fname_xpath = '//*[@id="modal-profile-edit"]/modal-profile-edit/div[2]/div/div[1]/div/div/form/div[1]'
        input_lname_xpath = '//*[@id="modal-profile-edit"]/modal-profile-edit/div[2]/div/div[1]/div/div/form/div[2]'

        self.wait_for_update(input_fname_xpath, 'xpath')
        input_fname_element = self.driver.find_element(By.XPATH, input_fname_xpath)
        input_lname_element = self.driver.find_element(By.XPATH, input_lname_xpath)
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")

        input_fname_element.clear()
        input_fname_element.send_keys(fname)

        input_lname_element.clear()
        input_lname_element.send_keys(lname)

        file_input.send_keys(profile_path)

        ok_btn_xpath = '//*[@id="modal-avatar-resize"]/div/modal-avatar-resize/button/div/div'
        ok_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, ok_btn_xpath)))
        ok_btn = self.driver.find_element(By.XPATH, ok_btn_xpath)
        ok_btn.click()

        final_btn_xpath = '//*[@id="modal-profile-edit"]/modal-profile-edit/div[2]/button/div/div'
        final_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, final_btn_xpath)))
        final_btn = self.driver.find_element(By.XPATH, final_btn_xpath)
        final_btn.click()
        self.wait_for_update(edit_xpath, 'xpath')


class SoroushLogin(BaseLogin):
    def __init__(self, phonenumber):
        super(SoroushLogin, self).__init__(phonenumber)

        self.go_to_site(settings.LOGIN_SOROUSH)

    def main(self):
        self.wait_for_update('sign-in-phone-number', 'id')
        self.insert_phonenumber()
        self.wait_for_update('registration-first-name', 'id')
        self.name_input('sajjad', 'daneshmand', settings.PICTURE_PATH)
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
        time.sleep(3)
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


soroush = SoroushLogin('989394551092')
soroush.main()
