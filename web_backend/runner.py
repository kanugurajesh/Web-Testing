# import the FastAPI class
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from elasticsearch import Elasticsearch
import json

# create an instance of the FastAPI class
app = FastAPI()

# connect to the Elasticsearch cluster
es = Elasticsearch(['localhost:9200'])

# specify the index name
cluster_name = "final_cluster"

# allowing CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# add the CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
# create a function to return the schema as JSON which is read from the schema.json file
async def root(request: Request):
    # await request.json()
    with open("schema.json") as f:
        schema = json.load(f)
    schema = schema["mappings"]["properties"]
    # return the schema as JSON
    return JSONResponse(content=schema)


@app.post("/items/")
async def read_root(request: Request):
    es = Elasticsearch(['localhost:9200'])
    item = await request.json()
    with open("schema.json") as f:
        schema = json.load(f)
    option = []
    item = item["name"]
    heave = item.split(":")
    button = heave[0]

    # if schema["mappings"]["properties"][button]["type"] == "text":
    #     button = button + ".keyword"
    if heave[1] == "text":
        button = button + ".keyword"
    search_query = {
        "aggs": {
            "my_agg": {
                "terms": {
                    "field": button
                }
            }
        }
    }
    try:
        response = es.search(index="final_cluster", body=search_query)
    except Exception as e:
        print("Error querying Elasticsearch:", e)

    for bucket in response["aggregations"]["my_agg"]["buckets"]:
        option.append(bucket["key"])
    return option

@app.post("/item/")
async def read_root(request: Request):
    item = await request.json()
    mime = []
    status = []
    lists = []
    keys = []

    split_data = item["name"].split(":")
    field = split_data[0]
    
    field_value = item["text"]

    if split_data[1] == "integer" or split_data[1] == "boolean" or split_data[1] == "float":
        field_value = int(field_value)
    else:
        field = field + ".keyword"
        
    query = {
        "size": 0,
        "aggs": {
            "logs_by_day": {
                "date_histogram": {
                    "field": "epoch",
                    "fixed_interval": "1d"
                },
                "aggs": {
                    "logs_by_status": {
                        "terms": {
                            "field": field
                        },
                        "aggs": {
                            "logs_by_mimeType": {
                                "terms": {
                                    "field": "status",
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    query_1 = {
        "size": 0,
        "aggs": {
            "logs_by_day": {
                "date_histogram": {
                    "field": "epoch",
                    "fixed_interval": "1d"
                },
                "aggs": {
                    "logs_by_status": {
                        "terms": {
                            "field": field
                        },
                        "aggs": {
                            "logs_by_status": {
                                "terms": {
                                    "field": "mimeType.keyword",
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    with open("delete.txt", "r") as f:
        delete = f.read()

    result = es.search(index="final_cluster", body=query)

    j = 0

    for i in result["aggregations"]["logs_by_day"]["buckets"]:
        if j == 1:
            mime.append(i)
        else:
            if delete == i["key_as_string"]:
                j = 1
                mime.append(i)

    result = es.search(index="final_cluster", body=query_1)

    j = 0

    for i in result["aggregations"]["logs_by_day"]["buckets"]:
        if j == 1:
            status.append(i)
        else:
            if delete == i["key_as_string"]:
                j = 1
                status.append(i)

    print("The mime is ",mime)
    print("The status is ",status)

    lists = []
    
    for i in mime:
        dicts = {}
        dicts["name"] = i["key_as_string"]
        dicts["total_count"] = i["doc_count"]
        for j in i["logs_by_status"]["buckets"]:
            if j["key"] == field_value:
                for k in j["logs_by_mimeType"]["buckets"]:
                    dicts[k["key"]] = k["doc_count"]
        lists.append(dicts)

    for i in status:
        for j in i["logs_by_status"]["buckets"]:
            if j["key"] == field_value:
                for k in j["logs_by_status"]["buckets"]:
                    for l in lists:
                        if l["name"] == i["key_as_string"]:
                            l[k["key"]] = k["doc_count"]

    keys.extend(lists[0].keys())
    print("The list is ",lists)
    print("The key is ",keys)
    return {"mime": lists, "status": keys}