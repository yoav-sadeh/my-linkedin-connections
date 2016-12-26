__author__ = 'yoav'

from linkedin_model import LinkedInPage, EntityType
import unittest
from unittest import TestCase
from mock import mock

def con_filter(emp):
    return emp.shared_connections != None and len(emp.shared_connections) > 0

def search_connections(credentials, company_name, company_site):
    # go to linkedin and login
    linked_in = LinkedInPage(credentials[0], credentials[1])  # todo: transfer to config
    # search entities of type company by name
    search_results_page = linked_in.search(EntityType.Companies, company_name)
    # get entities(data objects) - reduce by previews filter
    company_iterator = search_results_page.get_entities_iterator(lambda x: x.name.lower().strip(' ') == company_name)
    # filter by web_site as unique identifier
    refined_search = [ent for ent in company_iterator if ent.web_site == company_site]

    for result in refined_search:
        # search result page is generic - go_to_result_page in this case will yield a company_page
        company_page = search_results_page.go_to_result_page(result)
        company_employees_page = company_page.go_to_employees_page()
        employees_with_connections = filter(con_filter, company_employees_page.entities_previews)
        linked_in.close()
        return employees_with_connections

def print_shared_connections(credentials, company_name, web_site):
    employees_with_connections = search_connections(credentials, company_name, web_site)
    print 'In {} you have shared connections with:'.format(company_name)
    for emp in employees_with_connections:
        print '{}: {}'.format(emp.name, emp.shared_connections)

class LinkedInTest(TestCase):

    def test_mes_couille(self):
        self.assertEqual(True,True)

if __name__ == '__main__':
    unittest.main()

