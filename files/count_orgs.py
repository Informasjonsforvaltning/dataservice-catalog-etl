import json
import urllib.request
import argparse
import requests

output_file = open('./tmp/publishers.txt', 'w')

inputfileName = "./tmp/dataservices_transformed_demo.json"


def count(data):
    # Transforming according to rules in README
    publishers = []
    for dataservice in data:
        publishers.append(dataservice["organizationId"])
    return publishers


with open(inputfileName) as json_file:
    data = json.load(json_file)
    # Transform the organization object to publisher format:
    pubs = count(data)
    for orgnr in pubs:
        output_file.write(orgnr + "\n")
