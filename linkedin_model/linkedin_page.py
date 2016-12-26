__author__ = 'yoav'

from entity_type import EntityType
from try_monad import Try
from search_results_page import SearchResultsPage
from page import RootPage



class LinkedInPage(RootPage):

    def __init__(self, mail, pwd):
        super(LinkedInPage, self).__init__('http://linkedin.com')

        def login(mail, password):
            mail_elem = self.browser.find_element_by_id('login-email')
            pass_elem = self.browser.find_element_by_id('login-password')
            submit_btn = self.browser.find_element_by_id('login-submit')
            mail_elem.send_keys(mail)
            pass_elem.send_keys(password)
            submit_btn.click()

        try:
            login(mail, pwd)
        except Exception as e:
            self.log_exception_and_quit('Could not login to LinkedIn, quitting session.', e)

    def search(self, entity_type, entity_name):
        try:
            self.set_search_type(entity_type)
            search_box = self.browser.find_element_by_id('main-search-box')
            search_box.send_keys(entity_name)
            submit = self.browser.find_element_by_class_name('search-button')
            submit.click()
            return SearchResultsPage(self.browser, self)
        except Exception as e:
            self.log_exception_and_quit('Could not perfome LinkedIn search, quitting session.', e)

    def set_search_type(self, entity_type):
        try:
            search_drop_down_and_click = Try(lambda: self.browser.find_element_by_class_name('styled-dropdown-select-all')).map(lambda x: x.click()) #search-selector')
            #search_drop_down.click()

            search_type_slector_and_click = search_drop_down_and_click.map(lambda: self.browser.find_element_by_xpath('//li[contains(@class, "{}")]'.format(entity_type.name.lower()))).map(lambda x: x.click())
            #search_type_slector.click()
        except Exception as e:
            self.log_exception_and_quit('Could not set search type, quitting session.', e)


