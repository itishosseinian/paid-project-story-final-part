import json
import csv

# Load JSON data
json_file = 'output.json'  # Replace with your JSON file

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
    data = [data]  # Wrap in a list to avoid KeyError if it's a single dictionary

# Write to CSV
csv_file = 'output.csv'  # Desired CSV file name
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Write the header
    writer.writerow(data[0].keys())

    # Write the data
    for row in data:
        writer.writerow(row.values())
