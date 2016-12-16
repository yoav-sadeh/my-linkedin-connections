__author__ = 'yoav'

from company_page import CompanyPage
from page import *
from previews import *
from people_page import PeoplePage
from entity_type import EntityType
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SearchResultPage(Page):
    def __init__(self, browser):
        super(SearchResultPage, self).__init__(browser)

        def get_results_type(results):
            if len(results) == 0:
                return EntityType.None
            else:
                the_type = results[0].get_attribute('class').split(' ')[-1:][0]
                if the_type == 'company':
                    return EntityType.Companies
                elif the_type == 'people':
                    return EntityType.People
                else:
                    return EntityType.Jobs

        def get_results_element():

            element = WebDriverWait(self.browser, 5).until( #todo: move timeouts to config
            EC.presence_of_element_located((By.ID, "results")))
            return element

        def get_result_element(results, idx):
            element = results.find_elements_by_xpath('child::li')[idx]
            return element

        def map_results(elem):
            if entity_type == EntityType.Companies:
                yield CompanyPreview(elem)
                yield elem
            elif entity_type == EntityType.People:
                yield PersonPreview(elem)
                yield elem
            else:
                yield JobPreview(elem)
                yield elem

        try:
            results_elements = get_results_element().find_elements_by_xpath('child::li')
            entity_type = get_results_type(results_elements)
            time.sleep(1)

            mapped_results = dict(map(map_results, results_elements))
            self.results = mapped_results.keys()
        except NoSuchElementException as e:
            print e

        def go_to_entity_page(search_result):
            mapped_results[search_result].find_element_by_class_name('entity-img').click()

            return CompanyPage(self.browser, self)

        self.go_to_entity_page = go_to_entity_page

class SearchResultsPage(EntityAggregatorPage):
    def __init__(self, browser, page):
        super(SearchResultsPage, self).__init__(browser, page)

    def go_to_result_page(self, search_result_preview):

        entity_type = self.entity_service.get_entity_type()

        return self.go_to_entity_page(search_result_preview, self.type_to_ctor[entity_type])

    type_to_ctor = {
        EntityType.People: PeoplePage,
        EntityType.Companies: CompanyPage
    }