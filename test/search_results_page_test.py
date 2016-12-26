__author__ = 'yoav'

import sys
sys.path.append('../linkedin_model')
sys.path.append('.')
import unittest
from unittest import TestCase
from mock import mock,Mock
from linkedin_model.linkedin_page import LinkedInPage, EntityType
from linkedin_model.try_monad import Try

class SearchResultsPageTest(TestCase):

    @mock.patch('linkedin_model.page.DriverServices')
    @mock.patch('linkedin_model.page.EntityServices')
    def test_wrong_preview(self, mock_entity_service, mock_driver):
        li_page = LinkedInPage("mail", "pwd")
        results_page = li_page.search(EntityType.Companies, 'some company')

        results_page.entities_previews = [Mock(), Mock(), Mock()]
        mock_entity_service.return_value.get_entity_type.return_value = EntityType.Companies
        result_page = Try(lambda: results_page.go_to_result_page(Mock()))

        mock_driver.return_value.quit.assert_called



if __name__ == '__main__':
    unittest.main()