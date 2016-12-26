__author__ = 'yoav'

import sys
sys.path.append('../linkedin_model')
sys.path.append('.')
import mock
import unittest
from unittest import TestCase
from selenium.common.exceptions import NoSuchElementException
from linkedin_model.try_monad import Try
from mock import mock,Mock
from linkedin_model.linkedin_page import LinkedInPage, EntityType
from linkedin_model.company_page import CompanyPage
from selenium.webdriver.common.by import By
#/usr/local/Cellar/python/2.7.8_2/bin/python
class CompanyPageTest(TestCase):

    @mock.patch('linkedin_model.page.DriverServices')
    @mock.patch('linkedin_model.page.EntityServices')
    def test_company_view_more_failure(self, mock_entity_service, mock_driver):

        li_page = LinkedInPage("mail", "pwd")
        #mock_driver.return_value.find_element_by_id.side_effect = NoSuchElementException

        search_results_page = li_page.search(EntityType.Companies, 'amamam')
        search_results_page.entities_previews = [Mock(), Mock(), Mock()]
        mock_entity_service.return_value.get_entity_type.return_value = EntityType.Companies
        company_iterator = search_results_page.go_to_entity_page(search_results_page.entities_previews[0])
        mock_driver.return_value.try_get_element.assert_any_call((By.CLASS_NAME, 'show-details'))
        mock_driver.return_value.try_get_element.assert_any_call((By.CLASS_NAME, 'view-more-bar'))
        mock_driver.return_value.quit.assert_called()

    @mock.patch('linkedin_model.page.DriverServices')
    @mock.patch('linkedin_model.page.EntityServices')
    def test_goto_employees_page_failure(self, mock_entity_service, mock_driver):

        company_page = CompanyPage(mock_driver, None)
        company_page.go_to_employees_page()
        mock_driver.try_get_element.assert_any_call((By.CLASS_NAME, 'more'))
        #mock_driver.return_value.try_get_element.assert_any_call((By.CLASS_NAME, 'view-more-bar'))
        mock_driver.quit.assert_called()

if __name__ == '__main__':
    unittest.main()