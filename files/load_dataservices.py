import json
import os
from pymongo import MongoClient
import argparse
from bson.objectid import ObjectId

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()
connection = MongoClient(
    f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@mongodb:27017/dataservice-catalog?authSource=admin&authMechanism=SCRAM-SHA-1""")
db = connection['dataservice-catalog']

with open(args.outputdirectory + 'transformed_dataservices.json') as datasets_file:
    transformed_json = json.load(datasets_file)

    total_updated = 0
    total_failed = 0
    for mongo_id in transformed_json:
        to_be_updated = transformed_json[mongo_id]
        print("Updating ID: " + mongo_id)
        insert_result = db.dataservices.find_one_and_update({'_id': ObjectId(mongo_id)},  {'$set': to_be_updated})
        if insert_result:
            total_updated += 1
            print("Successfully updated: " + mongo_id)
        else:
            total_failed += 1
            print("Update failed: " + mongo_id)
    print("Total number of dataservices updated: " + str(total_updated))
    print("Total number of dataservice updates failed: " + str(total_failed))
