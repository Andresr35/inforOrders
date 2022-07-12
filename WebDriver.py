from selenium import webdriver

class EnviromentSetUp(webdriver.Chrome):

    @classmethod
    def setUp(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        cls.web=webdriver.Chrome(options=options)

    @classmethod
    def closeWeb(cls):
        if(cls.web==None):
            cls.web.quit()