import json

# Create a dictionary to store the mapping
mapper = {"mappings":{"properties":{}}}

# Open the JSON file and iterate through the objects
with open('./network_log/network_0_log.json') as f:
    for obj in json.load(f):
        for key, value in obj.items():
            value_type = type(value).__name__
            if value_type == 'int':
                mapper["mappings"]["properties"].setdefault(key, {"type": "integer"})
            elif value_type == 'float' or value_type == 'double' or value_type == 'long' or value_type == 'short':
                mapper["mappings"]["properties"].setdefault(key, {"type": "float"})
            elif value_type == 'bool':
                mapper["mappings"]["properties"].setdefault(key, {"type": "boolean"})
            elif value_type == 'date':
                mapper["mappings"]["properties"].setdefault(key, {"type": "date"})
            else:
                mapper["mappings"]["properties"].setdefault(key, {"type": "text"})
    # Add the epoch field
    # mapper["mappings"]["properties"].setdefault("epoch", {"type": "date"})
# Write the mapping to a JSON file
with open('schema.json', 'w') as f:
    mapper["mappings"]["properties"]["epoch"] = {"type": "date"}
    json.dump(mapper, f, indent=2)