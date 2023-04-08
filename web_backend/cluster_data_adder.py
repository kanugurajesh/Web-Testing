from elasticsearch import Elasticsearch
import json
import os

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200/'])
dir_name = 'network_logs_elasticsearch'
dir_path = os.path.join(os.getcwd(),dir_name)

# Delete the cluster if it exists
cluster_name = "final_cluster"

# check if a file exists
# if os.path.exists("num.txt"):
#     with open("num.txt", 'r') as f:
#         i = int(f.read())
# else:
#     i = 0

# Iterate through all the JSON files in the directory and load them into Elasticsearch
for file in os.listdir(dir_path):
    with open(os.path.join(dir_path,file)) as f:
        jsona = json.load(f)
        for doc in jsona:
            # i += 1
            es.index(index=cluster_name,body=doc)

# with open("num.txt", 'w') as f:
#     f.write(str(i))