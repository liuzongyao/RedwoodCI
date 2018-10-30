from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from actions.open_browser import Browser


class UI:
    def __init__(self):
        self.data_dir = './bin/'

    def goto_url(self, params):
        url = params.get('url')
        Browser.driver.get(url)
        # driver.refresh()

    def find(self, params):

        key = params.get('type')
        value = params.get('value')
        if key == 'id':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.ID, value))
            # return driver.find_element(By.ID, value)

        elif key == 'class_name':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.CLASS_NAME, value))
            # return driver.find_element(By.CLASS_NAME, value)

        elif key == 'css_selector':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, value))

            # return driver.find_element(By.CSS_SELECTOR, value)
        elif key == 'link_text':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.LINK_TEXT, value))
            # return driver.find_element(By.LINK_TEXT, value)

        elif key == 'tag_name':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.TAG_NAME, value))

        elif key == 'name':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.NAME, value))
            # return driver.find_element(By.NAME, value)
        elif key == 'partial_link_text':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.PARTIAL_LINK_TEXT, value))
            # return driver.find_element(By.PARTIAL_LINK_TEXT, value)
        elif key == 'xpath':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_element(By.XPATH, value))
            # return driver.find_element(By.XPATH, value)
        else:
            pass

    def find_all(self, params):

        key = params.get('type')
        value = params.get('value')
        if key == 'id':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.ID, value))
            # return driver.find_element(By.ID, value)

        elif key == 'class_name':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.CLASS_NAME, value))
            # return driver.find_element(By.CLASS_NAME, value)

        elif key == 'css_selector':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.CSS_SELECTOR, value))

            # return driver.find_element(By.CSS_SELECTOR, value)
        elif key == 'link_text':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.LINK_TEXT, value))
            # return driver.find_element(By.LINK_TEXT, value)

        elif key == 'tag_name':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.TAG_NAME, value))

        elif key == 'name':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.NAME, value))
            # return driver.find_element(By.NAME, value)
        elif key == 'partial_link_text':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.PARTIAL_LINK_TEXT, value))
            # return driver.find_element(By.PARTIAL_LINK_TEXT, value)
        elif key == 'xpath':
            return WebDriverWait(Browser.driver, 10).until(lambda x: x.find_elements(By.XPATH, value))
            # return driver.find_element(By.XPATH, value)
        else:
            pass

    def click(self, params):

        self.find(params).click()

    def set_text(self, params):

        self.find(params).clear()

        self.find(params).send_keys(params.get('Text'))

    def close(self):
        Browser.driver.close()

    def assert_text_in(self, params):
        text = params.get('Text')
        elements = self.find_all(params)
        for i in range(len(elements)):
            text_find = elements[i].text
            print text_find
            if text_find == text:
                assert True

    def assert_text_not_in(self, params):
        text = params.get('Text')
        elements = self.find_all(params)
        for i in range(len(elements)):
            text_find = elements[i].text
            print text_find
            if text_find == text:
                assert False
