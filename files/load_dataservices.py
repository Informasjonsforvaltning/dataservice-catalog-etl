import json
import urllib.request
import argparse


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

        req = urllib.request.Request(uploadUrl, json.dumps(dataservice).encode("utf-8"), headers={'content-type': 'application/json', 'accept': 'application/json'}, method='PATCH')

        try:
            rsp = urllib.request.urlopen(req)
            output_file.write(f'{rsp.code}' + ': ' + dataservice + "\n")

        except urllib.error.HTTPError as err:
            print(f'{err.code}' + ': ' + dataservice["title"])
            error_file.write(f'{err.code}' + ': ' + dataservice + "\n")
