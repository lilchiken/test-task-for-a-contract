from pathlib import Path

import pytest
import yaml

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def config():
    path = Path(__file__).parent.parent.joinpath('config.yaml')
    try:
        with open(path) as config:
            data = yaml.load(config, yaml.FullLoader)
        return data
    finally:
        config.close()


class BaseTest:

    @pytest.fixture(autouse=True)
    def init_webdriver(self):
        browser = config()['browser']
        if browser == 'Chrome':
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(
                service=ChromeService(
                    ChromeDriverManager().install()
                ),
                options=options
            )
        elif browser == 'Firefox':
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(
                service=FirefoxService(
                    GeckoDriverManager().install()
                ),
                options=options
            )
        else:
            raise Exception("Incorrect Browser")
        
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

        yield self.wait, self.driver

        if self.driver:
            self.driver.close()
            self.driver.quit()
