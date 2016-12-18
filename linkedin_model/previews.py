__author__ = 'yoav'

from selenium.common.exceptions import NoSuchElementException

#todo: try to remove and remove inheritance from children(is hash and eq method working?)
class Preview(object):
    def __init__(self, element):
        pass


class CompanyPreview(Preview):
    def __init__(self, element):
        super(CompanyPreview, self).__init__(element)

        self.name = element.find_element_by_xpath('div/h3').text

    def __eq__(self, other):
        return other.name == self.name

    def __hash__(self):
        return self.name.__hash__()


class PersonPreview(Preview):
    def __init__(self, element):
        super(PersonPreview, self).__init__(element)
        def get_name(element):
            return element.find_element_by_class_name('main-headline').text
        def get_job_title(element):
            description_element = element.find_element_by_class_name('description')
            title = description_element.text

            return title

        self.name = get_name(element)
        self.job_title = get_job_title(element)
        try:
            shared_conn_elements = element.find_element_by_class_name('expansion-container').find_element_by_tag_name('ol').find_elements_by_xpath('child::li')
            self.shared_connections = [e.find_element_by_xpath('div/h4/a').text for e in shared_conn_elements]
        except NoSuchElementException:
            self.shared_connections = None


class JobPreview(Preview):
    def __init__(self, element):
        super(JobPreview, self).__init__(element)
        def get_job_description(element):pass
        def get_company_name(element):pass

        self.job_description = get_job_description(element)
        self.company_name = get_company_name(element)

