from selenium import webdriver
from configparser import ConfigParser

class ChromeService:
    def __init__(self, selenium_executable_path : str, user_agent : str, headless : bool = False) -> None:
        self.selenium_executable_path = selenium_executable_path
        self.user_agent = user_agent
        self.headless = headless

    def get_cookies(self, config_path : str) -> list[dict]:
        cfg = ConfigParser()
        cfg.read(config_path)

        laravel_session_key = cfg["Linkvertise"]["SESSION_KEY"]
        xsrf_key = cfg["Linkvertise"]["XSRF_KEY"]

        return [
        {
            "domain": "publisher.linkvertise.com",
            "expirationDate": 2**31,
            "name": "laravel_session",
            "path": "/",
            "session": 'false',
            "storeId": "0",
            "value": laravel_session_key,
            "id": 1
        },
        {
            "domain": "publisher.linkvertise.com",
            "expirationDate": 2**31,
            "name": "XSRF-TOKEN",
            "path": "/",
            "session": 'false',
            "storeId": "0",
            "value": xsrf_key,
            "id": 2
        }]

    def setup_driver(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        options.add_argument(f"user-agent={self.user_agent}")
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-logging")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--window-size=1920,1080")

        if (self.headless): options.add_argument("--headless")

        self.core = webdriver.Chrome(executable_path = self.selenium_executable_path, options = options, service_log_path="Logs\\driver.log")

        self.core.maximize_window()

        self.core.get("https://publisher.linkvertise.com/dashboard")
        self.core.delete_all_cookies()

        cookies = self.get_cookies(config_path = "./settings.ini")

        for cookie in cookies:
            self.core.add_cookie(cookie)
        
        self.core.refresh()