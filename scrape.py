"""Scrapes data from ListReports.com"""

import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import StaleElementReferenceException

from auth import handle_login
from utils import get_last_id
from config import (
    EMAIL,
    PASSWORD,
    LOGIN_URL,
    MAIN_URL,
    COOKIE_FILE,
    EMAILS_FILE,
    GLOBAL_TIMEOUT,
)

service: ChromeService = ChromeService()
driver: webdriver.Chrome = webdriver.Chrome(service=service)

handle_login(driver, COOKIE_FILE, EMAIL, PASSWORD, LOGIN_URL)
driver.get(MAIN_URL)

NAMES_XPATH = "//div[@class='sc-ksYbfQ haFBVt']"
EMAIL_XPATH = "//p[contains(text(), 'Email:')]/following-sibling::p/a"
AGENT_NAME_XPATH = ".//span[@class='MuiButton-label']/b"

# Wait for the agents list to be present
agents = WebDriverWait(driver, GLOBAL_TIMEOUT).until(
    EC.presence_of_all_elements_located((By.XPATH, NAMES_XPATH))
)

# Wait a few seconds so that the user can manually apply filters
time.sleep(15)

while True:
    try:
        # Wait for the agents list to be present
        agents = WebDriverWait(driver, GLOBAL_TIMEOUT).until(
            EC.presence_of_all_elements_located((By.XPATH, NAMES_XPATH))
        )

        last_id = get_last_id(EMAILS_FILE)
        num = last_id + 1 if last_id > 0 else 0
        while num < 1200:
            # Before scraping the data, check if we need to load more rows
            while num >= len(agents) - 1:
                try:
                    # Find the "View more" button and click it
                    view_more_button = WebDriverWait(
                        driver, GLOBAL_TIMEOUT
                    ).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='View more']")
                        )
                    )
                    view_more_button.click()

                    # Wait for the agents list to be present
                    agents = WebDriverWait(driver, GLOBAL_TIMEOUT).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, NAMES_XPATH)
                        )
                    )

                    time.sleep(2)  # Give time for more rows to load

                except Exception as e:
                    print("Error clicking 'View more' button:", e)

            try:
                agent = agents[num]

                # Scroll to the client element to ensure it's in view
                driver.execute_script("arguments[0].scrollIntoView();", agent)

                # Extract agent's name
                agent_name = agent.find_element(
                    By.XPATH, AGENT_NAME_XPATH
                ).text

                # Click the client element
                agent.click()

                # Wait for the email element to be present and clickable
                email_link = WebDriverWait(driver, GLOBAL_TIMEOUT).until(
                    EC.element_to_be_clickable((By.XPATH, EMAIL_XPATH))
                )

                # Get the href attribute of the <a> element
                email_href = email_link.get_attribute("href")

                # Extract the email address from the href attribute
                email_address = email_href.split(":")[1]

                # emails.append(email_address)
                agent_details = {
                    "id": num,
                    "name": agent_name,
                    "email": email_address,
                }

                # Save the collected emails to a JSON file
                with open("emails.json", mode="a", encoding="utf-8") as file:
                    json.dump(agent_details, file)
                    file.write("\n")

                # Go back to the main page
                driver.execute_script("window.history.go(-1);")

                # Wait for the agents list to be present
                agents = WebDriverWait(driver, GLOBAL_TIMEOUT).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, NAMES_XPATH)
                    )
                )

                # if num == 5:
                #     break
                time.sleep(2)
                num += 1

            except Exception as e:
                print("An error occurred:", e)

    except StaleElementReferenceException:
        # If this exception occurs, refresh the agents list and continue
        print(
            "Stale element reference. Refreshing agents list and continuing..."
        )
        continue

    except Exception as e:
        print("An error occurred:", e)
        break

# Close the driver when done
driver.quit()
