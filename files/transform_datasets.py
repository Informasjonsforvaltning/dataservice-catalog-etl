import json
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
new_base_uri = os.environ['FDK_REGISTRATION_BASE_URI']


def transform(inputfile):

    datasets = openfile(inputfile)
    transformed_datasets = {}
    print("Total number of extracted datasets: " + str(len(datasets)))
    for dataset_key in datasets:
        old_uri = datasets[dataset_key].get("uri")
        if old_uri:
            new_uri = create_uri(datasets[dataset_key])
            if old_uri != new_uri:
                transformed_datasets[old_uri] = new_uri
    return transformed_datasets


def create_uri(dataset):
    return new_base_uri + '/catalogs/' + dataset["org_id"] + "/datasets/" + dataset["ds_id"]


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


inputfileName = args.outputdirectory + "mongo_datasets.json"
outputfileName = args.outputdirectory + "transformed_datasets.json"


with open(outputfileName, 'w', encoding="utf-8") as outfile:
    json.dump(transform(inputfileName), outfile, ensure_ascii=False, indent=4)
