import time
from selenium import webdriver
import platform
from selenium.webdriver.chrome.options import Options as options1
from selenium.webdriver.firefox.options import Options as options2
from os import path   



class Browser:
    driver = None
    def run(self, params):
        if params.get('browser') == "Chrome":
            if platform.system() == 'Darwin':
                chrome_options = options1()
                chrome_options.add_argument("--headless")
                # driver = webdriver.Chrome('./bin/chromedrivermac',chrome_options=chrome_options)  # Optional argument, if not specified will search path.
                Browser.driver = webdriver.Chrome('../../bin/chromedrivermac')  # Optional argument, if not specified will search path.
                time.sleep(5)  # Let the user actually see something!
                Browser.driver.maximize_window()

            elif platform.system() == 'Linux':
                chrome_options = options1()
                chrome_options.add_argument("--headless")
                # driver = webdriver.Chrome('./bin/chromedriverlinux',chrome_options=chrome_options)  # Optional argument, if not specified will search path.
                Browser.driver = webdriver.Chrome('../../bin/chromedriverlinux')  # Optional argument, if not specified will search path.
                time.sleep(5)  # Let the user actually see something!
                Browser.driver.maximize_window()

            else:
                pass
        else:
            if platform.system() == 'Darwin':
                firefox_options = options2()
                firefox_options.headless = True
                Browser.driver = webdriver.Firefox(executable_path='/RedwoodHQ/public/automationscripts/Sample/admin/bin/geckodrivermac', options=firefox_options)
                time.sleep(5)
                Browser.driver.maximize_window()

            elif platform.system() == 'Linux':
                firefox_options = options2()
                firefox_options.headless = True
                Browser.driver = webdriver.Firefox(executable_path='/RedwoodHQ/public/automationscripts/Sample/admin/bin/geckodriverlinux',options=firefox_options)
                time.sleep(5)
                Browser.driver.maximize_window()

            else:
                pass
