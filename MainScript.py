from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import traceback
import time
import random
import string
from resources import constants
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

comments_path = constants.comments_path2_remote
num_of_articles = random.randint(5, 10)
comments_list = []

with open(comments_path) as f:
    lines = f.readlines()

for line in lines:
    comments_list.append(line)


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
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        # self.driver = webdriver.Chrome("/home/m/PycharmProjects/DVABot/resources/chromedriver", options=chrome_options)

    def deviant_art_login(self):
        username_xpath = '//*[@id="username"]'
        password_xpath = '//*[@id="password"]'
        login_xpath = '//*[@id="loginbutton"]'

        try:
            print("login to DA")
            self.driver.get('https://www.deviantart.com/users/login')
            time.sleep(10)
            print(self.driver.find_element_by_xpath(username_xpath).tag_name)
            self.driver.find_element_by_xpath(username_xpath).send_keys(self.username)
            self.driver.find_element_by_xpath(password_xpath).send_keys(self.password)
            time.sleep(5)
            self.driver.find_element_by_xpath(login_xpath).click()

            time.sleep(10)
            print("login successful!")
        except Exception as e:
            print(f"deviant_art_login issue at : ", e)
            print(traceback.format_exc())
            time.sleep(2)

    def scrape_written_content(self):
        fill_all_xpath = '//*[@id="fill_all"]'
        submit_xpath = '//*[@id="quick_submit"]'

        extracted_dict = {}
        for x in range(num_of_articles):
            try:
                print("scraping article number:")
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

                full_page_content = f"{my_content} \n https://crypto-money.is-the-best.xyz/"

                extracted_dict[x] = [story_title.title(), full_page_content]

            except Exception as e:
                print(f"the scraping issue at : ", e)
                print(traceback.format_exc())

        return extracted_dict

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

    def deviant_art_extract_links(self):
        link_el_selector = "a[data-hook*='deviation_link']"
        random_letter = random.choice(list(string.ascii_lowercase))
        deviation_links = []

        try:
            self.driver.get(f'https://www.deviantart.com/search?q={random_letter}')
            print("extracting deviation links...")
            time.sleep(5)
            link_elements = self.driver.find_elements_by_css_selector(link_el_selector)

            for el in link_elements:
                print(el.get_attribute('href'))
                deviation_links.append(el.get_attribute('href'))

        except Exception as e:
            print(f"deviant_art link extraction issue at : ", e)
            print(traceback.format_exc())
            time.sleep(2)

        print("number of links: ", len(deviation_links))

        return deviation_links

    def deviation_commenter(self, single_link, rand_comment):
        selector = "div[data-hook*='comments_thread']"
        comment_box_xpath = "//*[contains(text(), 'Add a new comment...')]"
        commentselector = "div[data-offset-key*='foo-0-0']"
        comment_btn_xpath = "//button[contains(.,'Cancel')]/following-sibling::button"
        try:
            self.driver.get(single_link)
            print(f"making comment on {single_link}")
            time.sleep(5)
            element = self.driver.find_element_by_css_selector(selector)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(5)
            self.driver.find_element_by_xpath(comment_box_xpath).click()
            time.sleep(2)
            self.driver.find_element_by_css_selector(commentselector).send_keys(rand_comment)
            time.sleep(5)
            btn_element = self.driver.find_element_by_xpath(comment_btn_xpath)
            ActionChains(self.driver).move_to_element(btn_element).click(btn_element).perform()
            time.sleep(5)
            print("commment posted!")
        except Exception as e:
            print(f"deviant_art link extraction issue at : ", e)
            print(traceback.format_exc())
            time.sleep(2)


if __name__ == "__main__":
    lb = LitBot("saber20k", 'q-MnK&5n"x#i#@F')

    # extracted_text_dict = lb.scrape_written_content()

    lb.deviant_art_login()
    # for i in range(len(extracted_text_dict)):
    #     print("submitting article number: ", i)
    #     lb.submit_words(extracted_text_dict.get(i)[0], extracted_text_dict.get(i)[1])

    # dev_links = lb.deviant_art_extract_links()
    #
    # for link in dev_links:
    #     random_comment = random.choice(comments_list)
    #     lb.deviation_commenter(link, random_comment)



