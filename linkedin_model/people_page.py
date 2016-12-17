__author__ = 'yoav'

from page import EntityAggregatorPage

class PeoplePage(EntityAggregatorPage):

    def __init__(self, browser, page):
        super(PeoplePage, self).__init__(browser, page)

        #self.people = self.extract_people() #todo:move all driver functions to a separate class for encapsulation and DRY

    def go_to_person_page(self, person_preview):
        self.go_to_entity_page(person_preview, PersonPage)

    def pre_process_elements(self):
        self.validate_ownership()
        previews = self.get_results_container().find_elements_by_xpath('child::li')
        for preview_element in previews:
            try:
                preview_element.find_element_by_class_name('shared-conn-expando').click()
            except Exception as e:
                print '{} does not have shared connections with you.'.format(preview_element.find_element_by_class_name('main-headline').text)


class PersonPage(EntityAggregatorPage):

    def __init__(self, browser, page):
        super(PersonPage, self).__init__(browser, page)
