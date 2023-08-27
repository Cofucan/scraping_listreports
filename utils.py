
import json
import os

from config import EMAILS_FILE


def get_last_id(filename: str) -> int:
    """Get the last id in the emails.json file"""
    if not os.path.exists(filename):
        return 0

    with open(filename, mode="r", encoding="utf-8") as file:
        # emails = json.load(file)
        emails = file.readlines()
        email = json.loads(emails[-1])

    return email["id"]


def check_table_loaded(driver) -> bool:
    """Wait for the table to get populated with data"""
    table_xpath = "//table[@class='sc-jTzLTM bqkMeN']"
    h1_xpath = "//h1[@class='MuiTypography-root MuiTypography-h1']"
    if driver.find_element(
        by="xpath", value=table_xpath
    ) and driver.find_element(by="xpath", value=h1_xpath):
        print("Table found, data loaded successfully")
        return True

    print("Data not loaded as expected")
    return False


if __name__ == "__main__":
    print(type(get_last_id(EMAILS_FILE)))
