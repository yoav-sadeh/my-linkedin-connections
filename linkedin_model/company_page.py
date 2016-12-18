__author__ = 'yoav'

from page import *
from people_page import PeoplePage
from previews import *
from entity_type import EntityType
from selenium.webdriver.common.by import By
from company import Company
from linkedin_model.try_monad import Success, Failure


class CompanyPage(EntityPage):

    # #todo: remove redundent
    # def back(self):
    #     super(CompanyPage, self).back()


    def __init__(self, browser, page):
        super(CompanyPage, self).__init__(browser, page)
        #self.browser = browser #todo: remove redundent

    # def initialize_content(self):
    #     super(CompanyPage, self).initialize_content()

    def extract_entity(self):
        view_more_bar = self.browser.try_get_element((By.CLASS_NAME, 'view-more-bar'))

        company = view_more_bar.map(self.new_company)

        if company.isFailure():
           view_more_bar = self.browser.try_get_element((By.CLASS_NAME, 'show-details'))
           company = view_more_bar.map(self.old_company)

        if company.isFailure():
            raise Exception('could not extract company for the following reason: {}'.format(company.exception.message))

        return company.value

    def new_company(self, view_more_bar):
        view_more_bar.click()
        basic_info = self.browser.find_element_by_class_name('basic-info-about')
        company_name = self.browser.find_element_by_xpath('//span[contains(@itemprop, "name")]').text
        web_site = basic_info.find_element_by_xpath('ul/li[contains(@class, "website")]').find_element_by_xpath(
            'p/a').text
        industry = basic_info.find_element_by_xpath('ul/li[contains(@class, "industry")]').text
        type = basic_info.find_element_by_xpath('ul/li[contains(@class, "type")]').text
        size = basic_info.find_element_by_xpath('ul/li[contains(@class, "size")]').text
        founded = basic_info.find_element_by_xpath('ul/li[contains(@class, "founded")]').text
        return Company(company_name, industry, type, size, founded, web_site)

    def old_company(self, view_more_bar):
        view_more_bar.click()
        basic_info = self.browser.find_element_by_class_name('company-meta-text')
        company_name = self.browser.find_element_by_xpath('//h1[contains(@class, "company-main-info-company-name")]').text
        web_site = basic_info.find_element_by_xpath('dl/dd[contains(@class, "company-page-url")]').find_element_by_xpath('child::a').text
        industry = basic_info.find_element_by_xpath('dl/dd[contains(@class, "industry")]').text
        type = basic_info.find_element_by_xpath('dl/dd[contains(@class, "company-type")]').text
        size = basic_info.find_element_by_xpath('dl/dd[contains(@class, "staff-count-range")]').text
        founded = basic_info.find_element_by_xpath('dl/dd[contains(@class, "founded-year")]').text
        return Company(company_name, industry, type, size, founded, web_site)


    def go_to_employees_page(self):
        if(self.session_owner):
            #snackbar-description-see-all-link
            view_more_element = self.browser.try_get_element((By.CLASS_NAME, 'more')) #find_element_by_class_name('more')
            view_more_element.map(lambda e: e.click())

            if view_more_element.isFailure():
                view_more_element = self.browser.try_get_element((By.CLASS_NAME, 'snackbar-description-see-all-link'))
            view_more_element.map(lambda e: self.browser.get(e.get_attribute('href')))

            if view_more_element.isFailure():
                message = 'could not go to user page for the following reason: {}'.format(view_more_element.exception.message)
                self.logger.error(message)
                raise Exception(message)
            #https://www.linkedin.com/vsearch/p?f_CC=1441
            return PeoplePage(self.browser, self)

        else:
            raise Exception("Operation not allowed: page isn't session owner")

