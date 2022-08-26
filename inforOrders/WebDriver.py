"""This page sets up the web driver to be used everywhere.
NOTE: Selenium usually calls their webdriver driver.
I called it web.


"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class EnviromentSetUp(webdriver.Chrome):

    @classmethod
    def setUp(cls):
        """This just sets up the options for the web driver. The web object can then be used to open
        sites and other selenium methods.

        Call closeWeb() to stop the driver.
        """

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # ChromDriverManager handles the driver for chrome instead of
        # requiring users to download the chrom driver on their own.
        cls.web = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)

    @classmethod
    def closeWeb(cls):
        if(cls.web == None):
            cls.web.quit()
