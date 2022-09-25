import pathlib

from os import getenv


BASE_DIR = pathlib.Path(__file__).parent


API_TOKEN = getenv("API_TOKEN")
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
DRIVER_PATH = BASE_DIR.joinpath("geckodriver.exe")
MAX_WORKERS = getenv("MAX_WORKERS", 3)
