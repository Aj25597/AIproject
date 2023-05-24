import csv
import json

# Read CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Convert data to JSON
def convert_to_json(data):
    return json.dumps(data)

# Main function
def main():
    # Specify the CSV file path
    csv_file = 'emails.csv'

    # Read CSV file
    data = read_csv(csv_file)

    # Convert data to JSON
    json_data = convert_to_json(data)

    # Print JSON data
    print(json_data)

# Execute the main function
if __name__ == '__main__':
    main()
