from typing import Dict

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):

    def __init__(self, driver, wait):
        self.url = "http://localhost/sign-in"
        super().__init__(driver, wait)

    def go_to_page(self):
        self.goto(self.url)

    def check_title(self, title) -> bool:
        assert self.get_title() == title

    def make_a_search(
        self,
        xpath_val: Dict[str, Dict[str, str]],
        result: str
    ) -> bool:
        self.driver.find_element(
            By.XPATH, xpath_val.get('username')['path']
        ).send_keys(xpath_val.get('username')['value'])
        self.driver.find_element(
            By.XPATH, xpath_val.get('password')['path']
        ).send_keys(xpath_val.get('password')['value'])
        self.driver.find_element(
            By.XPATH, xpath_val.get('button')['path']
        ).click()
        assert self.wait.until(
            EC.presence_of_element_located((By.XPATH, result)),
            "Проблема со страницей авторизации."
        )
        assert self.driver.current_url == "http://localhost/dashboard"