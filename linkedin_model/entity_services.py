__author__ = 'yoav'

from entity_type import EntityType
from previews import *

class EntityServices:

    def __init__(self, url):
        self.url = url

    def get_entity_type(self):
            if len(self.url) == 0: #todo:change to proper linkedin url regex
                return EntityType.None

            parts = self.url.split('//')[1].split('?')[0].split('/')
            if parts[1] == 'jobs':
                return EntityType.Jobs
            elif parts[-1] == 'p':
                return EntityType.People
            elif parts[-1] == 'c':
                return EntityType.Companies
            else:
                return EntityType.None

    def map_results(self, elem, expanded = False):
            entity_type = self.get_entity_type()
            if entity_type == EntityType.Companies:
                preview = CompanyPreview(elem)
                yield preview
                yield elem
            elif entity_type == EntityType.People:
                preview = PersonPreview(elem)
                yield preview
                yield elem
            elif entity_type == EntityType.Jobs:
                yield JobPreview(elem)
                yield elem
            else:
                raise Exception('Unknown entity')
