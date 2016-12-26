__author__ = 'yoav'

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from driver_services import DriverServices

class Locator(object):
    def __init__(self, by):
        self.by = by
        self.element = None

    def get(self, driver):
        self.element = driver.try_get_element(self.by)

    def get(self, element):
        self.element = element.try_get_element(self.by)


class LocatorElement(object):

    def __init__(self, elemnet):
        self.element = elemnet

    def click(self):
        self.element.map(lambda el: el.click())

    def type(self, text):
        self.element.send_keys(text)

