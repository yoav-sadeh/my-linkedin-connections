__author__ = 'yoav'

from page import *
from people_page import PeoplePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from previews import *
from entity_type import EntityType

class CompanyPage(Page):

    # #todo: remove redundent
    # def back(self):
    #     super(CompanyPage, self).back()


    def __init__(self, browser, page):
        super(CompanyPage, self).__init__(browser, page)
        #self.browser = browser #todo: remove redundent

    def initialize_content(self):
        super(CompanyPage, self).initialize_content()
        view_more_bar = WebDriverWait(self.browser, 5).until( #todo: move timeouts to config
            EC.presence_of_element_located((By.CLASS_NAME, "view-more-bar")))
        view_more_bar.click()
        basic_info = self.browser.find_element_by_class_name('basic-info-about') #todo: wrap with wait
        self.web_site = basic_info.find_element_by_xpath('ul/li[contains(@class, "website")]').find_element_by_xpath('p/a').text
        self.industry = basic_info.find_element_by_xpath('ul/li[contains(@class, "industry")]').text
        self.type = basic_info.find_element_by_xpath('ul/li[contains(@class, "type")]').text
        self.size = basic_info.find_element_by_xpath('ul/li[contains(@class, "size")]').text
        self.founded = basic_info.find_element_by_xpath('ul/li[contains(@class, "founded")]').text


    def go_to_employees_page(self):
        if(self.session_owner):
            view_more_element = WebDriverWait(self.browser, 5).until( #todo: move timeouts to config
            EC.presence_of_element_located((By.CLASS_NAME, "more")))
            view_more_element.click()
            return PeoplePage(self.browser, self)

        else:
            raise Exception("Operation not allowed: page isn't session owner")

