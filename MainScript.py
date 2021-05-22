from selenium import webdriver
from selenium.webdriver.support.ui import Select
import traceback
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LitBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-dev-sgm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome("/home/m/PycharmProjects/DVABot/resources/chromedriver", options=chrome_options)

    def deviant_art_login(self):
        username_xpath = '//*[@id="username"]'
        password_xpath = '//*[@id="password"]'
        login_xpath = '//*[@id="loginbutton"]'

        try:
            self.driver.get('https://www.deviantart.com/users/login')
            time.sleep(5)
            self.driver.find_element_by_xpath(username_xpath).send_keys(self.username)
            self.driver.find_element_by_xpath(password_xpath).send_keys(self.password)
            time.sleep(5)
            self.driver.find_element_by_xpath(login_xpath).click()

            time.sleep(10)

        except Exception as e:
            print(f"deviant_art_login issue at : ", e)
            print(traceback.format_exc())
            time.sleep(2)

    def extract_words(self):
        fill_all_xpath = '//*[@id="fill_all"]'
        submit_xpath = '//*[@id="quick_submit"]'
        story_title = ""
        full_page_content = ""
        try:
            time.sleep(5)
            self.driver.get('https://www.plot-generator.org.uk/story/')
            time.sleep(5)
            self.driver.find_element_by_xpath(fill_all_xpath).click()
            time.sleep(2)
            self.driver.find_element_by_xpath(submit_xpath).click()
            time.sleep(3)
            story_title = self.driver.title.split('|')[0]
            story_text = self.driver.find_element_by_class_name("blurb").text

            my_content = story_text.replace(". ", ". \n")

            full_page_content = f"{my_content} \n https://is-the-best.xyz/"

        except Exception as e:
            print(f"the scraping issue at : ", e)
            print(traceback.format_exc())

        return story_title.title(), full_page_content

    def submit_words(self, current_title, current_content):
        submit_xpath = '//*[@id="site-header-submit-button"]'
        lit_xpath = '//*[@title="Literature"]'
        content_xpath = '//*[@data-focused="1"]'
        title_xpath = '//*[@placeholder="Add your title here"]'
        submit_btn_xpath = "//button[contains(.,'Submit')]"
        frame_selector = "iframe[class*='iframed_submitform never-hide-me loaded active']"
        submit2_btn_selector = "button[class*='ile-button ile-heading-submit-button ile-handicapped ile-submit-button smbutton smbutton-green']"

        try:
            time.sleep(5)
            self.driver.find_element_by_xpath(submit_xpath).click()
            time.sleep(3)
            self.driver.find_element_by_xpath(lit_xpath).click()
            time.sleep(3)
            self.driver.find_element_by_xpath(content_xpath).send_keys(current_content)
            time.sleep(5)
            self.driver.find_element_by_xpath(title_xpath).send_keys(current_title)
            time.sleep(5)
            elements = self.driver.find_elements_by_xpath(submit_btn_xpath)
            elements[2].click()
            time.sleep(10)
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, frame_selector)))

            submit_now_btn = self.driver.find_element_by_css_selector(submit2_btn_selector)

            ActionChains(self.driver).move_to_element(submit_now_btn).click(submit_now_btn).perform()
            time.sleep(5)

            self.driver.switch_to.default_content()

        except Exception as e:
            print(f"deviant_art_login issue at : ", e)
            print(traceback.format_exc())
            time.sleep(2)


if __name__ == "__main__":
    lb = LitBot("saber20k", 'q-MnK&5n"x#i#@F')
    extracted_text = lb.extract_words()

    title = extracted_text[0]
    text = extracted_text[1]

    lb.deviant_art_login()
    lb.submit_words(title, text)


