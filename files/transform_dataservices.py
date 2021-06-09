import json
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()


def transform(inputfile, inputfile2):
    datasets = openfile(inputfile)
    dataservices = openfile(inputfile2)
    transformed_dataservices = {}
    print("Total number of extracted dataservices: " + str(len(dataservices)))
    for dataservice_key in dataservices:
        transformed = transform_dataservice(datasets, dataservices[dataservice_key])
        transformed_dataservices[dataservice_key] = transformed
    return transformed_dataservices


def transform_dataservice(dataset_uris, dataservice):
    transformed_serves_dataset = []
    for dataset_uri in dataservice.get("servesDataset"):
        new_uri = dataset_uris.get(dataset_uri)
        if new_uri:
            transformed_serves_dataset.append(new_uri)
        else:
            transformed_serves_dataset.append(dataset_uri)
    transformed_dataservice = {"servesDataset": transformed_serves_dataset}
    return transformed_dataservice


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "transformed_datasets.json"
inputfileName2 = args.outputdirectory + "mongo_dataservices.json"
outputfileName = args.outputdirectory + "transformed_dataservices.json"


with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName, inputfileName2), outfile, ensure_ascii=False, indent=4)
