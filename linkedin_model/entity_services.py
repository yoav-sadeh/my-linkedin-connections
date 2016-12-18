__author__ = 'yoav'

from entity_type import EntityType
from previews import *
from logger_factory import get_logger
from linkedin_model.try_monad import Try


class EntityServices:

    def __init__(self, url):
        self.url = url
        self.logger = get_logger(self)
        self.logger.debug(r'url: {}'.format(url))

    def get_entity_type(self):
            try:
                if len(self.url) == 0: #todo:change to proper linkedin url regex
                    raise Exception("Empty url!")

                parts = self.url.split('//')[1].split('?')[0].split('/')
                if parts[1] == 'jobs':
                    return EntityType.Jobs
                elif parts[-1] == 'p':
                    return EntityType.People
                elif parts[-1] == 'c':
                    return EntityType.Companies
                else:
                    return EntityType.None
            except:
                pass

    def map_results(self, elem):
            entity_type = self.get_entity_type()
            if entity_type == EntityType.Companies:
                preview = Try(lambda: CompanyPreview(elem))
                if preview.isFailure():
                    self.logger.error(preview.exception.message)
                return preview

            elif entity_type == EntityType.People:
                preview = Try(lambda: PersonPreview(elem))
                if preview.isFailure():
                    self.logger.error(preview.exception.message)
                return preview

            elif entity_type == EntityType.Jobs:
                return Try(lambda: JobPreview(elem))
            else:
                raise Exception('Unknown entity')
