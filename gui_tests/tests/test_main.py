import pytest

from pages.main_page import MainPage
from tests.base_test import BaseTest


class TestMain(BaseTest):
    """Тест мэйн страницы (авторизации)."""

    @pytest.fixture
    def load_pages(self):
        self.page = MainPage(self.driver, self.wait)
        self.page.go_to_page()

    def test_title(self, load_pages):
        self.page.check_title('Application Platform')

    def test_search(self, load_pages):
        self.page.make_a_search(
            xpath_val={
                'username': {
                    'path': '//*[@id="root"]/div[1]/div/main/form/div[1]/div/div/input',
                    'value': 'start_admin'
                },
                'password': {
                    'path': '//*[@id="root"]/div[1]/div/main/form/div[2]/div/div/input',
                    'value': 'starter12345'
                },
                'button': {
                    'path': '//*[@id="root"]/div[1]/div/main/form/div[4]/button'
                }
            },
            result='//*[@id="root"]/div[1]/header/div/div/button'
        )
