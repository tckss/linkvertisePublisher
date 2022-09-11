from src.Driver import ChromeService
from src.ToLongException import ToLongException
from src.ToShortException import ToShortException
from src.ArleadyHasLinkException import ArleadyHasLinkException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from configparser import ConfigParser
from colorama import init
from colorama import Fore, Back, Style

import logging
import time
import os

class LinkCreator:
    def __init__(self) -> None:
        cfg = ConfigParser()
        cfg.read("settings.ini")

        logging.basicConfig(
            level=logging.INFO,
            filename="Logs\\LinkCreator.log",
            filemode="w",
            format="%(asctime)s %(levelname)s %(message)s"
        )

        if (cfg["Linkvertise"]["headless"] == "True"): headless = True
        else: headless = False

        self.chromeService = ChromeService(selenium_executable_path = os.path.abspath("Chromedriver\\chromedriver.exe"), user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36", headless=headless)
        
        print(Fore.MAGENTA + "[!] initialization Chrome Service Core")
        self.chromeService.setup_driver()
    
    def create_link(self, main_link : str, link_number : str, title : str, description : str, cooldown : int) -> str:
        time.sleep(cooldown)

        create_link_button = self.chromeService.core.find_element(By.ID, "link-create-nav") # Finding "create link" button, then clicking
        create_link_button.click()

        time.sleep(cooldown)

        try:
            self.chromeService.core.find_element(By.CSS_SELECTOR, ".js-cookie-consent-agree.cookie-consent__agree").click()
        except:
            pass

        # with open("index.html", "w", encoding="utf-8") as html:
        #     html.write(self.chromeService.core.page_source)
        ###
        

        # p = self.chromeService.core.find_element_by_class_name("p-relative")
        # print(p.child)

        self.chromeService.core.switch_to.frame(self.chromeService.core.find_elements(By.TAG_NAME, "iframe")[17]) # Opening 18 frame because page has a lot of iframes, but this is currently
        
        ###

        logging.info("[!] Filling the forms...")
        print(Fore.MAGENTA + "\t[!] Filling the forms...")

        time.sleep(cooldown)

        link_input = self.chromeService.core.find_element(By.ID, "mat-input-0")
        # Finding the link input, then paste the link

        link_input.send_keys(main_link)

        waiter = WebDriverWait(self.chromeService.core, 10)

        # right_next_button = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-describedby=cdk-describedby-message-2]")))
        time.sleep(cooldown)

        try:
            right_next_button = self.chromeService.core.find_elements(By.CLASS_NAME, "mat-tooltip-trigger")[2]
            right_next_button.click()

            # self.chromeService.core.find_elements(By.CLASS_NAME, "mat-input-element")[0]
            # (By.ID, "mat-input-4")
            short_link_input = waiter.until(EC.element_to_be_clickable(self.chromeService.core.find_elements(By.CLASS_NAME, "mat-input-element")[0]))

            short_link_input.send_keys(link_number)
        
            waiter.until(EC.element_to_be_clickable(self.chromeService.core.find_elements(By.CSS_SELECTOR, "button.lv-action-button.lv-center")[0])).click()
        
        except:
            logging.error("Maybe, this link is arleady registred. Delete this from 'links.txt'!")
            raise ArleadyHasLinkException("Maybe, this link is arleady registred. Delete this from 'links.txt'! (RUS : вероятно, ссылка уже зарегестрирована. Удалите её из 'links.txt'")

        # short_link_input.click()
        # short_link_input.send_keys(Keys.ENTER)

        try:
            # 80 max
            if (len(title) <= 39):
                logging.error("Title string is too SHORT")
                raise ToShortException("Title string is too SHORT!")
            
            if (len(title) >= 81):
                logging.error("Title string is too LONG!")
                raise ToLongException("Title string is too LONG!")
            
            # self.chromeService.core.find_elements(By.CLASS_NAME, "mat-input-element")[1]
            # (By.ID, "mat-input-17")

            try:

                link_title_input = waiter.until(EC.element_to_be_clickable(self.chromeService.core.find_elements(By.CLASS_NAME, "mat-input-element")[1]))
                
                link_title_input.send_keys(title)

                waiter.until(EC.element_to_be_clickable(
                    self.chromeService.core.find_elements(By.CSS_SELECTOR, "button.lv-action-button.lv-center")[1]
                )).click()
            
            except Exception as ex:
                logging.error("Exception", exc_info=True)
            
            # time.sleep(cooldown + 2)
            # link_title_input.click()
            # link_title_input.send_keys(Keys.ENTER)
        
        except ElementNotInteractableException:
            raise ToLongException("Maybe your string for title is too long!")

        # self.chromeService.core.find_elements(By.CLASS_NAME, "mat-input-element")[2]

        # (By.ID, "mat-input-24")

        description_input = waiter.until(EC.element_to_be_clickable(
            self.chromeService.core.find_elements(By.CLASS_NAME, "mat-input-element")[2]
        ))

        try:
            
            if (len(description) <= 99):
                logging.error("Your description is too short!")
                raise ToShortException("Your description is too short!")

            description_input.send_keys(description)

            # self.chromeService.core.find_element(By.CSS_SELECTOR, "[key=description]").find_element(By.TAG_NAME, "button")

            confirm_button = waiter.until(EC.element_to_be_clickable(
                self.chromeService.core.find_element(By.CSS_SELECTOR, "[key=description]").find_element(By.TAG_NAME, "button")
            ))

            confirm_button.click()
        
        except ElementNotInteractableException:
            raise ToShortException("Maybe your description length is too short!")

        self.chromeService.core.find_element(By.CSS_SELECTOR, ".button-wrapper.lv-center-between").find_elements(By.TAG_NAME, "lv-button")[1].location_once_scrolled_into_view # Scrolling to bottom

        time.sleep(cooldown)
        
        # self.chromeService.core.find_elements(By.CLASS_NAME, "faq-placeholder")

        faq_forms = waiter.until(EC.element_to_be_clickable((By.CLASS_NAME, "faq-placeholder"))) # just wait when faq forms will be interactable

        faq_forms = self.chromeService.core.find_elements(By.CLASS_NAME, "faq-placeholder")[:3]

        faq_forms[0].click()

        for i in range(len(faq_forms)):
            
            waiter.until(EC.element_to_be_clickable(
                self.chromeService.core.find_elements(By.CLASS_NAME, "faq-title")[i]
            )).click()

            time.sleep(0.5)
            
        time.sleep(0.3)

        time.sleep(cooldown)
        
        # done_button = self.chromeService.core.find_elements(By.CLASS_NAME, "lv-center-between")[1].find_elements(By.TAG_NAME, "lv-button")[1]

        
        ###
        done_button = waiter.until(EC.element_to_be_clickable(self.chromeService.core.find_element(By.CSS_SELECTOR, ".button-wrapper.lv-center-between").find_elements(By.TAG_NAME, "lv-button")[1]))

        done_button.click()

        time.sleep(cooldown + 1.5)

        next_button = waiter.until(EC.element_to_be_clickable(self.chromeService.core.find_element(By.CSS_SELECTOR, ".button-wrapper.lv-center-between").find_elements(By.TAG_NAME, "lv-button")[1]))

        next_button.click()

        time.sleep(cooldown + 2)

        final_button = waiter.until(EC.element_to_be_clickable(self.chromeService.core.find_element(By.CSS_SELECTOR, ".button-wrapper.lv-center-between").find_elements(By.TAG_NAME, "lv-button")[1]))

        final_button.click()
        ### - This block must be reworked (very bad code) (maybe use for)

        time.sleep(cooldown + 4)

        search_input = waiter.until(EC.element_to_be_clickable(self.chromeService.core.find_element(By.ID, "link_list").find_elements(By.CLASS_NAME, "form-control-sm")[1]))
        search_input.send_keys(main_link)
        time.sleep(2)

        url = self.chromeService.core.find_element(By.ID, "link_list").find_element(By.CLASS_NAME, "download-link").find_element(By.TAG_NAME, "input").get_attribute("value")

        logging.info(f"\t[!] Saving the url {url}")
        print(Fore.MAGENTA + f"\t[!] Saving the url {url}")

        return url

def read_settings(encoding : str) -> list[dict]:
    settings = []
    with open("data\\links.txt", "r", encoding=encoding) as links, \
            open("data\\links_numbers.txt", "r", encoding=encoding) as links_numbers, \
            open("data\\title.txt", "r", encoding=encoding) as title, \
            open("data\\description.txt", "r", encoding=encoding) as description:
        
        links = [x.replace("\n", "") for x in links]
        links_numbers = [x.replace("\n", "") for x in links_numbers.readlines()]
        titles = [x.replace("\n", "") for x in title.readlines()]
        descriptions = [x.replace("\n", "") for x in description.readlines()]

        for i in range(len(links)):
            settings.append({
                "link" : links[i],
                "link_number" : links_numbers[i],
                "title" : titles[i],
                "description" : descriptions[i]
            })
    
    return settings

def main() -> None:
    cfg = ConfigParser()
    cfg.read("settings.ini")
    session, xsrf = cfg["Linkvertise"]["SESSION_KEY"], cfg["Linkvertise"]["XSRF_KEY"]
    encoding = cfg["Linkvertise"]["encoding"]

    init() # Colorama init
    print(Fore.RED + "********* PUBLISHER LINKVERTISE *********")
    print(Fore.RED + "python script for auto-creating urls at linkvertise.com")
    print(Fore.RED + "Created by tkcs_soft")
    print(Fore.RED + "Contacts : \nDiscord : tkcs#3802\nTelegram : @tkcsWR\nMail : NicolasSsh@yandex.ru")
    print(Fore.RED + "[0] Starting program...")
    print(Fore.RED + "[0] Importing modules...")
    print(Fore.RED + "[0] Logging to the site...\n")
    print(Fore.RED + "*" * 41)

    print(Fore.RED + "SETTINGS : \n")
    print(Fore.RED + f"SESSION KEY : {session[:-20]}" + "*" * 20)
    print(Fore.RED + f"XSRF KEY : {xsrf[:-280]}" + "*" * 20 + "\n")

    print(Fore.RED + "*" * 41 + "\n")
    
    lk = LinkCreator()
    settings = read_settings(encoding=encoding)


    for link in settings:
        try:
            print(Fore.CYAN + f"[!] working with url '{link['link']}'")
            logging.info(f"[!] working with url '{link['link']}'")

            url = lk.create_link(main_link = link["link"], link_number = link["link_number"], title = link["title"], description = link["description"], cooldown = 2)

            with open("data\\final_links.txt", "a") as final_file:

                final_file.write(url + "\n")
        
        except Exception as ex:
            logging.error("Exception", exc_info=True)

if __name__ == "__main__":
    main()