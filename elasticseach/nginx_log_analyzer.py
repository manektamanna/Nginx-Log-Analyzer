import argparse
import datetime
import json
import requests
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import BadRequestError


def index_json_to_elasticsearch() -> None:
    """
    Reads JSON data from a URL and indexes it to Elasticsearch.

    The script takes the following command-line arguments:
        url: the URL of the file to read
        index_name: the name of the Elasticsearch index to use
        elasticsearch_api: the URL of the Elasticsearch API endpoint
        username: the username to use for Elasticsearch authentication
        password: the password to use for Elasticsearch authentication
    """

    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Index data from JSON file to Elasticsearch")
    parser.add_argument("url", help="the URL of the file to read")
    parser.add_argument("index_name", help="the name of the Elasticsearch index to use")
    parser.add_argument("elasticsearch_api", help="the URL of the Elasticsearch API endpoint")
    parser.add_argument("username", help="the username to use for Elasticsearch authentication")
    parser.add_argument("password", help="the password to use for Elasticsearch authentication")
    args = parser.parse_args()

    # Define the Elasticsearch client with authentication
    if args.username and args.password:
        es = Elasticsearch(args.elasticsearch_api, http_auth=None, 
                           basic_auth=(args.username, args.password))
    else:
        es = Elasticsearch(args.elasticsearch_api)

    # Define the mapping for the index
    mapping = {
        "mappings": {
            "properties": {
                "time": {"type": "date"},
                "remote_ip": {"type": "ip"},
                "remote_user": {"type": "text"},
                "request": {"type": "text"},
                "response": {"type": "integer"},
                "bytes": {"type": "long"},
                "referrer": {"type": "text"},
                "agent": {"type": "text"}
            }
        }
    }

    # Create the index with the mapping
    es.indices.create(index=args.index_name, mappings=mapping, ignore=400)

    # Fetch the JSON data from the URL
    response = requests.get(args.url)
    data = response.content.decode().split("\n")

    # Loop through the lines and index each JSON object to Elasticsearch
    for line in data:
        if line.strip():
            # Parse the JSON object
            item = json.loads(line)

            try:
                # Convert time to datetime object
                time_obj = datetime.datetime.strptime(item["time"], "%d/%b/%Y:%H:%M:%S %z")
                item["time"] = time_obj

                # Convert response and bytes to integer or long data type
                item["response"] = int(item["response"])
                item["bytes"] = int(item["bytes"])

                # Index the document to Elasticsearch
                es.index(index=args.index_name, document=item)
            except ValueError as e:
                # Log the error to the console
                print(f"Error parsing document: {e}")
            except BadRequestError as e:
                # Log the error to the console
                print(f"Error indexing document: {e}")

if __name__ == '__main__':
    index_json_to_elasticsearch()