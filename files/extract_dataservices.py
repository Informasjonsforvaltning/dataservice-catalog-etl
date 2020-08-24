import json
import requests
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

data = json.loads('{"query":{"bool":{"must":[{"match_all":{}}],"must_not":[],"should":[]}},"from":0,"size":10000,"sort":[],"aggs":{}}')
host = 'http://elasticsearch5:9200/'
url = host + "/" + os.environ["ELASTIC_DATASERVICE_INDEX"] + "/_search"
headers = {'Content-Type': 'application/json'}

print("Posting to the following url: ", url)
print("Posting to publisher index the following data:\n", data)
# Load the publisher by posting the data:
r = requests.post(url, json=data, headers=headers)
with open(args.outputdirectory + 'dataservices.json', 'w', encoding="utf-8") as outfile:
    json.dump(r.json(), outfile, ensure_ascii=False, indent=4)
