__author__ = 'yoav'

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
from entity_services import EntityServices

class Page(object):

    session_owner = False
    def __init__(self, browser, page):
        self.browser = browser
        self.source_page = page
        self.take_page_over()

    def take_page_over(self):
        owning_page(self)
        self.initialize_content()


    def initialize_content(self):
        pass

    def back(self):
        self.browser.back()
        if self.source_page != None:
            time.sleep(1)
            self.source_page.take_page_over()

    def close(self):
        self.browser.quit()

    def validate_ownership(self):
        if(not self.session_owner):
            raise Exception("Operation not allowed: page isn't session owner")

class EntityAggregatorPage(Page):

    def __init__(self, browser, page):
        super(EntityAggregatorPage, self).__init__(browser, page)

    def initialize_content(self):
        super(EntityAggregatorPage, self).initialize_content()
        self.entity_service = EntityServices(self.browser.current_url)
        self.entities = self.extract_entities()


    def go_to_entity_page(self, preview, ctor):
        if type(ctor) is type(EntityAggregatorPage):
            self.get_preview_elements()[self.entities.index(preview)].find_element_by_class_name('entity-img').click()
            return ctor(self.browser, self) #todo: check possibility for additional args*

    def extract_entities(self):
        self.validate_ownership()
        self.pre_process_elements()
        results_elements = self.get_preview_elements()
        mapped_results = dict(map(self.entity_service.map_results, results_elements))
        return mapped_results.keys()

    def get_preview_elements(self):
        results_elements = self.get_results_container().find_elements_by_xpath('child::li')
        return results_elements

    def pre_process_elements(self):
        pass

    def get_results_container(self):
            element = WebDriverWait(self.browser, 5).until( #todo: move timeouts to config
            EC.presence_of_element_located((By.ID, "results")))
            return element


class RootPage(Page):
    browser = webdriver.Firefox()
    def __init__(self, page=None):
        super(RootPage, self).__init__(self.browser, page)

pages = set()

def owning_page(page):
    pages.add(page)
    page.session_owner = True
    for p1 in [p for p in pages if p != page]:
        p1.session_owner = False
