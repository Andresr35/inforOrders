import os
import sys
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def resource_path(relative_path: str) -> str:
    """gets the absolute path from the relative path

    Args:
        relative_path (str): in the local dir

    Returns:
        str: abs path
    """
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, relative_path)

class EnviromentSetUp(webdriver.Chrome):

    @classmethod
    def setUp(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        cls.web = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    @classmethod
    def closeWeb(cls):
        if(cls.web == None):
            cls.web.quit()
