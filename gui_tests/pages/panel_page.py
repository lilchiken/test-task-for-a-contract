from typing import Dict

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class PanelPage(BasePage):

    def __init__(self, driver, wait):
        self.url = "http://localhost/sign-in"
        super().__init__(driver, wait)

    def go_to_page(self):
        self.goto(self.url)
        self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[1]/div/main/form/div[1]/div/div/input'
        ).send_keys('start_admin')
        self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[1]/div/main/form/div[2]/div/div/input'
        ).send_keys('starter12345')
        self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[1]/div/main/form/div[4]/button'
        ).click()
        assert self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div[1]/header/div/div/button')
            ),
            "Проблема со страницей авторизации."
        )
        assert self.driver.current_url == "http://localhost/dashboard", (
            "Проблема с авторизацией."
        )

    def check_title(self, title) -> bool:
        assert self.get_title() == title

    def make_a_search(
        self,
        xpath_val: Dict[str, Dict[str, str]],
        result: str
    ) -> bool:
        self.driver.find_element(
            By.XPATH, xpath_val.get('button_upload')['path']
        ).click()
        self.driver.find_element(
            By.XPATH, xpath_val.get('file')['path']
        ).send_keys(xpath_val.get('file')['value'])

        url = "http://localhost/dashboard?modalOpen=true"

        assert self.driver.current_url == url, self.driver.current_url

        self.driver.find_element(
            By.XPATH, xpath_val.get('button_create')['path']
        ).click()

        assert self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="root"]/div[1]/header/div/div/button')
            )
        )

        self.goto('http://localhost/dashboard')

        assert self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div[1]/main/div/div/div[2]/table/tbody/tr[1]/td[2]')
            ),
            "Элемент не появился на странице"
        )

        assert result == self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[1]/main/div/div/div[2]/table/tbody/tr[1]/td[2]'
        ).text, "Элемент не появился на странице"