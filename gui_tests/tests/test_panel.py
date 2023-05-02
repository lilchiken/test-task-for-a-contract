from pathlib import Path
import random
from string import ascii_letters

import pytest

from pages.panel_page import PanelPage
from tests.base_test import BaseTest


class TestMain(BaseTest):
    """Тест панели управления (dashboard)."""

    @pytest.fixture
    def load_pages(self):
        self.page = PanelPage(self.driver, self.wait)
        self.page.go_to_page()

    @pytest.fixture()
    def file_for_test(self):
        self.name_file = ''.join(
            random.choice(ascii_letters) for _ in range(8)
        )
        self.path = Path(__file__).parent.parent.joinpath(
            '{}.txt'.format(self.name_file)
        )

        with open(self.path, 'w+') as file:
            file.write('some')
            file.close()
        yield self.path, self.name_file
        self.path.unlink()


    def test_title(self, load_pages):
        self.page.check_title('Application Platform')

    def test_search(self, load_pages, file_for_test):
        self.page.make_a_search(
            {
                'button_upload': {
                    'path': '//*[@id="root"]/div[1]/main/div/div/div[1]/button'
                },
                'file': {
                    # 'path': '//*[@id="upload_file"]'
                    'path': '//*[@id="upload_file"]',
                    'value': self.path.__str__()
                },
                'button_create': {
                    'path': '/html/body/div[2]/div[3]/div/div[3]/button[2]'
                }
            },
            self.name_file
        )