# importing the required modules
import json
import os
from datetime import datetime

# Get the current working directory
directory_path = os.getcwd()

directory_name = 'network_logs_elasticsearch'

directory_write = directory_path + '/' + directory_name

if os.path.exists(directory_write):
    for file in os.listdir(directory_write):
        os.remove(os.path.join(directory_write, file))

# Enter the directory name where network log are stored
network_log_directory = 'network_log'

if not os.path.exists(directory_write):
    os.mkdir(directory_write)

# Load the schema from json_schema.json
with open('schema.json', 'r') as f:
    schema = json.load(f)

# Loop through all the files in the network_log directory
for file in os.listdir(directory_path+"/"+network_log_directory):
    # Check if the file is a json file
    if file.endswith(".json"):
        # Load the json file
        with open(directory_path+'/'+network_log_directory+'/'+file, 'r') as f:
            print(file)
            json_objects = json.load(f)
        # Loop through all the json objects in the json file
        for json_object in json_objects:
            # Loop through all the keys in the schema
            for key in schema['mappings']['properties']:
                # Check if the key is not in the json object
                if key not in json_object:
                    data = schema['mappings']['properties'][key]['type']
                    # Add the key to the json object with a value of None
                    # json_object[key] = None
                    # check the type of the key in the schema
                    if data == 'integer':
                        # Add the key to the json object with a value of 0
                        json_object[key] = -1
                    elif data == 'float':
                        # Add the key to the json object with a value of 0.0
                        json_object[key] = -1.0
                    elif data == 'boolean':
                        # Add the key to the json object with a value of False
                        json_object[key] = False
                    else:
                        # Add the key to the json object with a value of ''
                        json_object[key] = "null"
        # Write the updated json objects to the json file
        with open(directory_write+"/"+file, 'w') as f:
            json.dump(json_objects, f, indent=2)