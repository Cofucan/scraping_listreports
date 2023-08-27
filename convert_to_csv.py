import json
import csv

# Open the JSON file for reading
with open("emails.json", "r", encoding="utf-8") as json_file:
    json_data = json_file.readlines()

# Initialize a list to hold the JSON objects
data_list = []

# Parse each JSON line and append to the list
for json_line in json_data:
    data = json.loads(json_line)
    data_list.append(data)

# Determine the keys for the CSV header
csv_header = data_list[0].keys()

# Open the CSV file for writing
with open("data.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)

    # Write the CSV header
    csv_writer.writeheader()

    # Write each data object as a row in the CSV
    for data in data_list:
        csv_writer.writerow(data)

print("Conversion complete")
