from collections import Counter
from print_dict import print_dict as prettyPrintMyListOfDicts
import importlib
import json
import os

DEBUG = importlib.import_module("1-Scrape").DEBUG
CACHE_DIR_NAME = importlib.import_module("1-Scrape").CACHE_DIR_NAME
SUGGESTION_THRESHOLD = 5


def deserialize(fileName):
    filePath = f"{CACHE_DIR_NAME}/{fileName}.json"
    if not os.path.exists(filePath):
        if DEBUG:
            print(f"File '{filePath}' does not exist.")
        exit(1)
    try:
        with open(filePath, "r") as jsonFile:
            data = json.load(jsonFile)
            if DEBUG:
                print(f"Data successfully read from '{filePath}'.")
            return data
    except Exception as e:
        print(f"Error occurred while deserializing '{filePath}': {e}")
        exit(1)


def buildFreqTable(listOfDicts, shouldSerialize=False):
    freqTable = Counter()
    for record in listOfDicts:
        freqTable.update(record["following"])
    freqDict = dict(freqTable)
    suggestDict, discardDict = {}, {}
    for key, value in freqDict.items():
        if key == None:
            continue
        if value >= SUGGESTION_THRESHOLD:
            suggestDict[key] = value
        else:
            discardDict[key] = value
    suggestDict = dict(sorted(suggestDict.items(), key=lambda item: item[1], reverse=True))
    discardDict = dict(sorted(discardDict.items(), key=lambda item: item[1], reverse=True))
    if shouldSerialize:
        serialize = importlib.import_module("1-Scrape").serialize
        serialize("suggest", suggestDict)
        serialize("discard", discardDict)
    if DEBUG:
        prettyPrintMyListOfDicts(suggestDict)
    return suggestDict, discardDict


if __name__ == "__main__":
    buildFreqTable(deserialize("seed"), shouldSerialize=True)
    print("SUCCESS")
