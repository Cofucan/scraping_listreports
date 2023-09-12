""" This module handles the convertion of the json data to csv. """
import json
import csv
import sys
import os


def json_to_csv(json_file_path: str, csv_file_path: str) -> None:
    """
    Converts a JSON file to a CSV file.

    Args:
        json_file_path (str): The path to the JSON file.
        csv_file_path (str): The path to the CSV file.

    Returns:
        None

    Example:
        ```python
        json_to_csv("input.json", "output.csv")
        ```
    """
    # Check if the CSV file exists
    csv_exists: bool = os.path.exists(csv_file_path)

    # Open the JSON file for reading
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_data = json_file.readlines()

    # Initialize a list to hold the JSON objects
    data_list: list = []

    # Parse each JSON line and append to the list
    for json_line in json_data:
        data = json.loads(json_line)
        data_list.append(data)

    # Determine the keys for the CSV header
    csv_header = data_list[0].keys()

    # Open the CSV file for writing in append mode if it exists, or create a new file if it doesn't exist
    with open(
        csv_file_path, "a" if csv_exists else "w", newline="", encoding="utf-8"
    ) as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)

        # If the CSV file is newly created, write the header
        if not csv_exists:
            csv_writer.writeheader()

        # Write each data object as a row in the CSV
        for data in data_list:
            csv_writer.writerow(data)

    print("Conversion complete")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <json_file_path> <csv_file_path>")
        sys.exit(1)

    JSON_PATH: str = sys.argv[1]
    CSV_PATH: str = sys.argv[2]

    json_to_csv(JSON_PATH, CSV_PATH)
