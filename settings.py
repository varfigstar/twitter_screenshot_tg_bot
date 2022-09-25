import pathlib
from os import getenv
import platform


BASE_DIR = pathlib.Path(__file__).parent


API_TOKEN = getenv("API_TOKEN")
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
if platform.system() == "Windows":
    print("Windows system")
    DRIVER_PATH = BASE_DIR.joinpath("geckodriver.exe")
else:
    print("Linux system")
    DRIVER_PATH = BASE_DIR.joinpath("geckodriver")
MAX_WORKERS = int(getenv("MAX_WORKERS", 3))
