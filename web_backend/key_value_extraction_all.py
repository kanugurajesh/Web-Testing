# importing the required modules
import json
import os
from datetime import datetime
import re

# Get the current working directory
curr_dir = os.getcwd()

# Define the path to the JSON file
json_directory = os.path.join(curr_dir, 'network_logs')

# Define the path to the JSON file
write_directory = os.path.join(curr_dir, 'network_log')

if os.path.exists(write_directory):
    for file in os.listdir(write_directory):
        os.remove(os.path.join(write_directory, file))

def dater(date_string):
    date_object = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %Z')
    iso8601_date_string = date_object.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return iso8601_date_string


# # Define a function to extract key-value pairs with immediate values
def extract_immediate(json_obj):
    extracted = {}
    # Check if the object is a dictionary
    if isinstance(json_obj, dict):
        # iterating over the dictionary
        for key, value in json_obj.items():
            # Check if the value is a dictionary or list
            if isinstance(value, dict) or isinstance(value, list):
                extracted.update(extract_immediate(value))
            else:
                extracted[key] = value
    # Check if the object is a list
    elif isinstance(json_obj, list):
        for item in json_obj:
            # Check if the item is a dictionary or list
            if isinstance(item, dict) or isinstance(item, list):
                extracted.update(extract_immediate(item))
    # Return the extracted dictionary
    return extracted

# check if the directory exists
if not os.path.exists(write_directory):
    os.mkdir('network_log')

# Loop through all the files in the network_log directory
for element in os.listdir(json_directory):
    # assigning the path to the variable
    json_file_path = os.path.join(json_directory, element)
    # Open and read the JSON file
    with open(json_file_path, "r") as file:
        json_data = json.loads(file.read())

    # open the file in write and append mode
    with open(f"{write_directory}/{element}", 'a+') as r:
        # iterate over each object in the JSON file
        for i, json_obj in enumerate(json_data):
            immediate_pairs = extract_immediate(json_obj)
            # check if file is empty
            if i == 0:
                r.write('[')
            else:
                r.write(',')
            # write the extracted dictionary to the output file
            try:
                dates = immediate_pairs["date"]
            except KeyError:
                dates = immediate_pairs["Date"]
            immediate_pairs["epoch"] = dater(dates)
            json.dump(immediate_pairs, r)
        # close the JSON list
        r.write(']')