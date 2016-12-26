__author__ = 'yoav'


import sys
sys.path.append('../linkedin_model')
sys.path.append('.')
import unittest
from unittest import TestCase
from selenium.common.exceptions import NoSuchElementException

from linkedin_model.try_monad import Try
from mock import mock,Mock
from linkedin_model.linkedin_page import LinkedInPage, EntityType

class LinkedInPageTest(TestCase):


    @mock.patch('linkedin_model.page.DriverServices')
    def test_initialization_failure(self, mock_driver):
        mock_driver.return_value.find_element_by_id.side_effect = NoSuchElementException
        li_page = Try(lambda: LinkedInPage("mail", "pwd"))

        mock_driver.return_value.quit.assert_called()

    @mock.patch('linkedin_model.page.DriverServices')
    def test_search_failure(self, mock_driver):

        li_page = Try(lambda: LinkedInPage("mail", "pwd"))
        mock_driver.return_value.find_element_by_id.side_effect = NoSuchElementException
        #li_page.map(lambda p: p.search(EntityType.Company, 'amamam'))
        li_page.value.search(EntityType.Companies, 'amamam')
        mock_driver.return_value.quit.assert_called()

    @mock.patch('linkedin_model.page.DriverServices')
    def test_set_search_type_failure(self, mock_driver):

        li_page = Try(lambda: LinkedInPage("mail", "pwd"))
        mock_driver.return_value.find_element_by_class_name.side_effect = NoSuchElementException
        li_page.value.search(EntityType.Companies, 'amamam')
        mock_driver.return_value.quit.assert_called()


if __name__ == '__main__':
    unittest.main()