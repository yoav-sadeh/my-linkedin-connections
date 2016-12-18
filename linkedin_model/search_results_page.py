__author__ = 'yoav'

import time

from linkedin_model.company_page import CompanyPage
from page import *
from previews import *
from people_page import PeoplePage
from entity_type import EntityType


class SearchResultsPage(EntityAggregatorPage):
    def __init__(self, browser, page):
        super(SearchResultsPage, self).__init__(browser, page)

    def go_to_result_page(self, search_result_preview):

        entity_type = self.entity_service.get_entity_type()

        return self.go_to_entity_page(search_result_preview)

    def entity_type_to_ctor(self):
        return {
        EntityType.People: PeoplePage,
        EntityType.Companies: CompanyPage
    }
