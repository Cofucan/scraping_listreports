import configparser

config = configparser.ConfigParser()
config.read("options.ini")

EMAIL: str = config.get("Main", "email")
PASSWORD: str = config.get("Main", "password")
LOGIN_URL: str = config.get("Main", "login_url")
MAIN_URL: str = config.get("Main", "main_url")
COOKIE_FILE: str = config.get("Main", "cookie_file")
EMAILS_FILE: str = config.get("Main", "emails_file")
CHROMEDRIVER_PATH: str = config.get("Main", "CHROMEDRIVER_PATH")
GLOBAL_TIMEOUT: int = config.getint("Main", "GLOBAL_TIMEOUT")
