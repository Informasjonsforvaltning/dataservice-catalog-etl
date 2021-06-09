import json
import os
from pymongo import MongoClient
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/dataservice-catalog?authSource=admin&authMechanism=SCRAM-SHA-1""")

db = connection['dataservice-catalog']
dict_list = list(db.dataservices.find())
dataservices = {}
for id_dict in dict_list:
    id_str = str(id_dict["_id"])
    dataservices[id_str] = {}
    dataservices[id_str]["servesDataset"] = id_dict.get("servesDataset")

print("Total number of extracted dataservices: " + str(len(dataservices)))

with open(args.outputdirectory + 'mongo_dataservices.json', 'w', encoding="utf-8") as outfile:
    json.dump(dataservices, outfile, ensure_ascii=False, indent=4)
