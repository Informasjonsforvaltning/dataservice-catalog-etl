import json
import urllib.request
import argparse
import requests


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

output_file = open('./tmp/load_dataservices_output.txt', 'w')
error_file = open('./tmp/load_dataservices_errors.txt', 'w')

inputfileName = args.outputdirectory + "dataservices_transformed.json"

with open(inputfileName) as json_file:
    count = 0
    data = json.load(json_file)
    for dataservice in data:
        uploadUrl = 'http://dataservice-catalog:8080/catalogs/' + dataservice['organizationId'] + '/dataservices'

        json_data = json.dumps(dataservice)

        try:
            rsp = requests.patch(uploadUrl, json_data, headers={'content-type': 'application/json', 'accept': 'application/json'})
            rsp.raise_for_status()
            output_file.write(f'{rsp.status_code}' + ': ' + json_data + "\n")

        except requests.HTTPError as err:
            print(f'{err}' + ': ' + dataservice["title"].get("nb"))
            error_file.write(f'{err}' + ': ' + json_data + "\n")
