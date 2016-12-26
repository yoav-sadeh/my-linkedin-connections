__author__ = 'yoav'

from page import EntityAggregatorPage, EntityPage
from linkedin_model.try_monad import Try


class JobsPage(EntityAggregatorPage):

    def __init__(self, browser, page):
        super(JobsPage, self).__init__(browser, page)

        #self.people = self.extract_people() #todo:move all driver functions to a separate class for encapsulation and DRY

    def go_to_person_page(self, person_preview):
        self.go_to_entity_page(person_preview, JobPage)

    def pre_process_elements(self):
        self.validate_ownership()
        previews = self.get_results_container().find_elements_by_xpath('child::li')

        for preview_element in previews:
            try:
                preview_element.find_element_by_class_name('shared-conn-expando').click()
            except Exception as e:
                tryLog = Try(lambda: self.logger.debug('{} does not have shared connections with you.'.format(preview_element.find_element_by_class_name('main-headline').text)))
                if tryLog.isFailure():
                    self.logger.debug('Spotted bizzare preview element with text: {}'.format(preview_element.text.encode('ascii', 'ignore')))



class JobPage(EntityPage):

    def __init__(self, browser, page):
        super(JobPage, self).__init__(browser, page)
