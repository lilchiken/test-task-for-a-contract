from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver, wait) -> None:
        # Нотация хрома, как пример, webdriver -
        # родительский класс не имеет методов
        self.driver: webdriver.Chrome = driver
        self.wait: WebDriverWait = wait

    def goto(self, url: str):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title
