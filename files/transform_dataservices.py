import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()


def transform(data):
    # Transforming according to rules in README
    array = data["hits"]["hits"]
    print(len(array))
    newArray = []
    transformed = []
    count = 0
    for dataservice in array:
        if dataservice["_source"].get("harvestStatus") and dataservice["_source"].get("harvestStatus")["success"]:
            contact = parseContact(dataservice["_source"]["apiSpecification"]["info"].get("contact"))
            dataservice_transformed = {"created": dataservice["_source"]["_lastModified"],
                                       "modified": dataservice["_source"]["_lastModified"],
                                       "organizationId": dataservice["_source"]["catalogId"],
                                       "operationCount": countPaths(dataservice["_source"]["apiSpecification"].get("paths")),
                                       "title": {"nb": dataservice["_source"]["apiSpecification"]["info"]["title"]},
                                       "version": dataservice["_source"]["apiSpecification"]["info"]["version"],
                                       "contact": {"name": contact.get("name"),
                                                   "url": contact.get("url"),
                                                   "email": contact.get("email")
                                                   },
                                       "endpointUrls": mapEndpointURL(dataservice["_source"]["apiSpecification"].get("servers")),
                                       "endpointDescriptions": dataservice["_source"]["apiSpecUrl"],
                                       "mediaTypes": dataservice["_source"]["apiSpecification"].get("formats"),
                                       "description": {"nb": dataservice["_source"]["apiSpecification"]["info"].get("description")},
                                       "license": dataservice["_source"]["apiSpecification"]["info"].get("license"),
                                       "access": {"isAuthoritativeSource": dataservice["_source"].get("isNationalComponent"),
                                                  "isOpenAccess": dataservice["_source"].get("isOpenAccess"),
                                                  "isOpenLicense": dataservice["_source"].get("isOpenLicense"),
                                                  "isFree": dataservice["_source"].get("isFree")
                                                  },
                                       "termsAndConditions": {"price": {"nb": dataservice["_source"].get("cost")},
                                                              "usageLimitation": {"nb": dataservice["_source"].get("usageLimitation")},
                                                              "capacityAndPerformance": {"nb": dataservice["_source"].get("performance")},
                                                              "reliability": {"nb": dataservice["_source"].get("availability")}},
                                       "externalDocs": dataservice["_source"]["apiSpecification"].get("externalDocs"),
                                       "dataServiceStatus": {"statusText": dataservice["_source"].get("statusCode"),
                                                             # "expirationDate": (),
                                                             # "comment": (),
                                                             # "supersededByUrl": ()
                                                             },
                                       "termsOfServiceUrl": dataservice["_source"]["apiSpecification"]["info"].get("termsOfService"),
                                       "serviceType": dataservice["_source"].get("serviceType"),
                                       "servesDataset": dataservice["_source"].get("datasetUris"),
                                       "status": dataservice["_source"].get("registrationStatus")
                                       # "imported": ()
                                       }
            newArray.append(dataservice_transformed)
        transformed = newArray
    print("Total to be transformed: ", len(newArray))
    return transformed


def mapEndpointURL(servers):
    endpointURLS = []
    for server in servers:
        endpointURLS.append(server["url"])
    return endpointURLS


def countPaths(paths):
    operationCount = 0
    if paths:
        for _ in paths:
            operationCount += 1
    return operationCount


def parseContact(info):
    return {"name": info.get("name") if info else None,
            "url": info.get("url") if info else None,
            "email": info.get("email") if info else None
            }


inputfileName = args.outputdirectory + "dataservices.json"
outputfileName = args.outputdirectory + "dataservices_transformed.json"

with open(inputfileName) as json_file:
    data = json.load(json_file)
    # Transform the organization object to publisher format:
    with open(outputfileName, 'w', encoding="utf-8") as outfile:
        json.dump(transform(data), outfile, ensure_ascii=False, indent=4)
