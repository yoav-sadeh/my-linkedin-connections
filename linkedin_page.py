__author__ = 'yoav'

from entity_type import EntityType
from search_results_page import SearchResultPage, SearchResultsPage
from page import RootPage
import time

class LinkedInPage(RootPage):

    def __init__(self, mail, pwd):
        super(LinkedInPage, self).__init__()
        self.browser.get('http://linkedin.com')
        self.browser.maximize_window()
        def login(mail, password):
            time.sleep(5)

            mail_elem = self.browser.find_element_by_id('login-email')
            pass_elem = self.browser.find_element_by_id('login-password')
            submit_btn = self.browser.find_element_by_id('login-submit')
            mail_elem.send_keys(mail)
            pass_elem.send_keys(password)
            submit_btn.click()

        login(mail, pwd)

    def search(self, entity_type, entity_name):
        self.set_search_type(entity_type)
        time.sleep(2)
        search_box = self.browser.find_element_by_id('main-search-box')
        search_box.send_keys(entity_name)
        submit = self.browser.find_element_by_class_name('search-button')
        submit.click()
        time.sleep(1)
        return SearchResultsPage(self.browser, self)


    def set_search_type(self, entity_type):
        search_drop_down = self.browser.find_element_by_class_name('styled-dropdown-select-all') #search-selector')
        search_drop_down.click()

        search_type_slector = self.browser.find_element_by_xpath('//li[contains(@data-li-styled-dropdown-class, "{}")]'.format(entity_type.name.lower()))
        search_type_slector.click()


