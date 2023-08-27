import pickle
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import COOKIE_FILE, MAIN_URL


def save_cookies(url: str) -> None:
    """
    Saves cookies on the current domain for future sessions. Useful in order
    to avoid having the need of filling the login details every time.

    Args:
        url: The URL of the website where the cookies will be stored.

    Returns:
        None
    """
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    pickle.dump(driver.get_cookies(), open(COOKIE_FILE, "wb"))


def handle_login(
    driver: webdriver.Chrome,
    cookie_file: str,
    user: str,
    paswd: str,
    url: str,
    timeout: int = 30,
) -> None:
    """
    Handles the login process.

    Args:
        driver: The driver object used to interact with the web browser.
        cookie_file: The path to the file where the cookies will be stored.
        user: The username to be used for login.
        paswd: The password to be used for login.
        url: The URL of the login page.
        timeout: The maximum time in seconds to wait for elements.

    Returns:
        None
    """
    driver.get(url)

    # Wait for email field to be present and enter username
    email_field = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    email_field.send_keys(user)

    # Wait for password field to be present and enter password
    password_field = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.send_keys(paswd)

    # Wait for login button to be clickable and click it
    submit_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_button.click()

    # Add sleep if needed
    time.sleep(9)

    # Save cookies to file
    pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))


def load_cookies(driver, cookie_file, url):
    """
    Load cookies into the specified WebDriver instance and navigate to the
    given URL.

    Parameters:
        driver (WebDriver): The WebDriver instance to load cookies into.
        cookie (str): The path to the cookie file to load.
        url (str): The URL to navigate to after loading the cookies.

    Returns:
        None
    """
    driver.get(url)
    time.sleep(3)
    cookies = pickle.load(open(cookie_file, "rb"))
    for cookie_file in cookies:
        # cookie['domain'] = '.listreports.com'
        driver.add_cookie(cookie_file)
    driver.refresh()


if __name__ == "__main__":
    save_cookies(MAIN_URL)
