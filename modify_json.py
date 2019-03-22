# modify json
import json

def writeToJson(data, file):
    with open(file, 'w') as outfile:
    json.dump(data, outfile)