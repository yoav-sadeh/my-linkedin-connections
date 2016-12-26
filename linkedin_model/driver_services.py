from linkedin_model.try_monad import Try

__author__ = 'yoav'

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from logger_factory import get_logger
from config_factory import get_config

class DriverServices(object):
    def __init__(self, initial_url):
        self.browser = webdriver.Firefox()#todo: enum to choose which browser to use
        self.browser.get(initial_url)
        self.browser.maximize_window()
        self.logger = get_logger(self)
        self.config = get_config()
        self.timeout = self.config.getint('DriverServices', 'timeout')


    def current_url(self):
            return self.browser.current_url

    def back(self):
        self.browser.back()

    def get(self, url):
        self.browser.get(url)

    def quit(self):
        self.browser.quit()

    def find_element_by_xpath(self, xpath):
        self.logger.debug('find_element_by_xpath: {}'.format(xpath))
        return WebDriverWait(self.browser, self.timeout ).until(EC.presence_of_element_located((By.XPATH, xpath)))


    def find_element_by_id(self, id):
        self.logger.debug('find_element_by_id: {}'.format(id))
        return WebDriverWait(self.browser, self.timeout ).until(EC.presence_of_element_located((By.ID, id)))

    def find_element_by_class_name(self, class_name):
        self.logger.debug('find_element_by_class_name: {}'.format(class_name))
        return WebDriverWait(self.browser, self.timeout ).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

    def find_elements_by_xpath(self, xpath):
        self.logger.debug('find_elements_by_xpath: {}'.format(xpath))
        return WebDriverWait(self.browser, self.timeout ).until(EC.presence_of_all_elements_located((By.CLASS_NAME, xpath)))

    def try_get_element(self, by):
        self.logger.debug('try_get_element: {}'.format(by))

        result = Try(lambda: WebDriverWait(self.browser, self.timeout ).until(EC.presence_of_element_located(by)))
        return result

    def try_get_elements(self, by):
        self.logger.debug('is_element_present: {}'.format(by))
        result = Try(lambda: WebDriverWait(self.browser, self.timeout ).until(EC.presence_of_all_elements_located(by)))
        return result

class ElementServices(object):
    def __init__(self, element):
        self.element = element
        self.logger = get_logger(self)
        self.config = get_config()
        self.timeout = self.config.getint('DriverServices', 'timeout')

    def find_element_by_xpath(self, xpath):
        self.logger.debug('find_element_by_xpath: {}'.format(xpath))
        return Try(lambda: self.element.find_element_by_xpath(xpath))


    def find_element_by_id(self, id):
        self.logger.debug('find_element_by_id: {}'.format(id))
        return Try(lambda: self.element.find_element_by_id(id))

    def find_element_by_class_name(self, class_name):
        self.logger.debug('find_element_by_class_name: {}'.format(class_name))
        return Try(lambda: self.element.find_element_by_class_name(class_name))


    def find_elements_by_xpath(self, xpath):
        self.logger.debug('find_elements_by_xpath: {}'.format(xpath))
        return Try(lambda: self.element.find_elements_by_xpath(xpath))

    def try_get_element(self, by):
        self.logger.debug('try_get_element: {}'.format(by))

        result = Try(lambda: self.element.find_element(by))
        return result

    def try_get_elements(self, by):
        self.logger.debug('is_element_present: {}'.format(by))
        result = Try(lambda: self.element.find_elements(by))
        return result
