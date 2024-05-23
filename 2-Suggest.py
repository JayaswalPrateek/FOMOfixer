from collections import Counter
from print_dict import print_dict as prettyPrintMyListOfDicts
import importlib
import json
import os

DEBUG = True
CACHE_DIR_NAME = "cache"


def deserialize(fileName):
    filePath = f"{CACHE_DIR_NAME}/{fileName}.json"
    if not os.path.exists(filePath):
        if DEBUG:
            print(f"File '{filePath}' does not exist.")
        return None
    try:
        with open(filePath, "r") as json_file:
            data = json.load(json_file)
            if DEBUG:
                print(f"Data successfully read from '{filePath}'.")
            return data
    except Exception as e:
        print(f"Error occurred while deserializing '{filePath}': {e}")
        return None


def buildFreqTable(listOfDicts):
    freqTable = Counter()
    for record in listOfDicts:
        freqTable.update(record["following"])
    freqDict = dict(freqTable)
    suggestDict = {}
    discardDict = {}
    for key, value in freqDict.items():
        if key == None:
            continue
        if value >= 5:
            suggestDict[key] = value
        else:
            discardDict[key] = value
    suggestDict = dict(
        sorted(suggestDict.items(), key=lambda item: item[1], reverse=True)
    )
    prettyPrintMyListOfDicts(suggestDict)
    # prettyPrintMyListOfDicts(discardDict)
    serialize = importlib.import_module("1-Scrape").serialize
    serialize("suggest", suggestDict)
    serialize("discard", discardDict)


if __name__ == "__main__":
    buildFreqTable(deserialize("seed"))
    print("SUCCESS")
