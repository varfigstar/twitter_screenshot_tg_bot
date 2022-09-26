import itertools

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import settings


class TwitterParser:
    def __init__(
            self,
    ):
        self.options = FirefoxOptions()
        # self.options.add_argument('--headless')
        self.driver = Firefox(
            executable_path=str(settings.DRIVER_PATH),
            options=self.options
        )

    def take_branch_screenshots(self, url, twit_depth=3) -> list[bytes]:
        print(f"Start task: {url} with depth: {twit_depth}")
        screenshots = []
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div[1]/div/div/div[2]/main/div/div/'
                    'div/div[1]/div/section/div/div/div[1]/div/div/'
                    'div/article/div/div/div/div[3]/div[2]/div/div/span'
                )
                )
            )
            elements = self.driver.find_elements(
                By.XPATH,
                '//div[@data-testid="cellInnerDiv"]'
            )
            for elem in elements:
                if len(screenshots) == twit_depth:
                    break
                try:
                    self.driver.set_window_size(
                        width=elem.size["height"],
                        height=self.driver.get_window_size()["height"] + elem.size["height"]
                    )
                    photo = elem.screenshot_as_png
                    if photo:
                        screenshots.append(photo)
                except:
                    ...
        except Exception as ex:
            print(ex)
        return screenshots


class ParsersPool:
    def __init__(
            self,
            parsers_num: int = 2,
    ):
        self.parsers = []
        self.round_parsers = None  # Round-robin parsers list
        self.parsers_num = parsers_num
        self._spawn_parsers()

    def _spawn_parsers(self):
        for i in range(self.parsers_num):
            parser = TwitterParser()
            self.parsers.append(parser)
        self.round_parsers = itertools.cycle(self.parsers)

    def take_screenshots(self, url, twit_depth):
        parser: TwitterParser = next(self.round_parsers)
        return parser.take_branch_screenshots(url, twit_depth)

