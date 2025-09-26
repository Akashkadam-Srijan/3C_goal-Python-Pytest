
class BrowserUtils:

    def __init__(self,driver):
        self.driver = driver

    def getPageTitle(self):
        return self.driver.title

