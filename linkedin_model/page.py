__author__ = 'yoav'

from driver_services import DriverServices
from logger_factory import get_logger

import time
from entity_services import EntityServices

class Page(object):

    session_owner = False
    def __init__(self, browser, page):
        self.logger = get_logger(self)
        self.logger.debug('entering page')
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

class EntityPage(Page):

    def __init__(self, browser, page):
        super(EntityPage, self).__init__(browser, page)

    def initialize_content(self):
        super(EntityPage, self).initialize_content()
        self.entity = self.extract_entity()

    def extract_entity(self):
        pass

class EntityAggregatorPage(Page):

    def __init__(self, browser, page):
        super(EntityAggregatorPage, self).__init__(browser, page)

    def initialize_content(self):
        super(EntityAggregatorPage, self).initialize_content()
        self.entity_service = EntityServices(self.browser.current_url())
        self.entities_previews = self.extract_entities_previews()

    def entity_type_to_ctor(self):
        pass

    def go_to_entity_page(self, preview):
        entity_type = self.entity_service.get_entity_type()
        ctor = self.entity_type_to_ctor()[entity_type]
        self.vaildate_page_ctor(ctor, preview)
        self.get_preview_elements()[self.entities_previews.index(preview)].find_element_by_class_name('entity-img').click()
        return ctor(self.browser, self)

    def vaildate_page_ctor(self, ctor, preview):
        if ctor == None:
            raise Exception('No constructor was given for preview: {}'.format(preview))
        if type(ctor) is not type(EntityAggregatorPage):
            raise Exception('Given constructor: {} for preview: {} is not of required type: EntityAggregatorPage '.format(ctor, preview))

    def extract_entities_previews(self):
        self.validate_ownership()
        self.pre_process_elements()
        results_elements = self.get_preview_elements()
        mapped_results = map(self.entity_service.map_results, results_elements)
        previews = map(lambda t: t.value, filter(lambda p: p.isSuccess(), mapped_results))
        return previews

    def get_preview_elements(self):
        results_elements = self.get_results_container().find_elements_by_xpath('child::li')
        return results_elements

    def pre_process_elements(self):
        pass

    def get_results_container(self):
            element = self.browser.find_element_by_id('results')
            return element

    def get_entities_iterator(self, previews_filter = None): #todo: implement as lazy iterator
        filtered_previews = filter(previews_filter, self.entities_previews) if previews_filter != None else self.entities_previews
        entities = []
        for preview in filtered_previews:
            entity_page = self.go_to_entity_page(preview)
            entities.append(entity_page.entity)
            entity_page.back()

        return entities



class RootPage(Page):
    def __init__(self, initial_url):
        browser = DriverServices(initial_url)
        super(RootPage, self).__init__(browser, None)

pages = set()

def owning_page(page):
    pages.add(page)
    page.session_owner = True
    for p1 in [p for p in pages if p != page]:
        p1.session_owner = False
