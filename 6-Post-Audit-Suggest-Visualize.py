from collections import defaultdict
import importlib
import os

SUGGESTION_THRESHOLD = importlib.import_module("2-Suggest").SUGGESTION_THRESHOLD


if __name__ == "__main__":
    oldDiscard = importlib.import_module("2-Suggest").deserialize("discard")
    oldSuggest = importlib.import_module("2-Suggest").deserialize("suggest")
    postAuditListOfDicts = importlib.import_module("2-Suggest").deserialize("seedDeltaPostAudit")
    newSuggest, newDiscard = importlib.import_module("2-Suggest").buildFreqTable(postAuditListOfDicts)
    mergedFreqTable = defaultdict(int)
    for key, value in oldDiscard.items():
        mergedFreqTable[key] += value
    for key, value in newSuggest.items():
        mergedFreqTable[key] += value
    for key, value in newDiscard.items():
        mergedFreqTable[key] += value
    for alreadyVisitedSuggestion in list(oldSuggest.keys()):
        if alreadyVisitedSuggestion in mergedFreqTable.keys():
            del mergedFreqTable[alreadyVisitedSuggestion]
    updatedSuggest = {key: value for key, value in mergedFreqTable.items() if value >= SUGGESTION_THRESHOLD}
    updatedDiscard = {key: value for key, value in mergedFreqTable.items() if value < SUGGESTION_THRESHOLD}

    updatedSuggest = dict(sorted(updatedSuggest.items(), key=lambda item: item[1], reverse=True))
    updatedDiscard = dict(sorted(updatedDiscard.items(), key=lambda item: item[1], reverse=True))

    importlib.import_module("3-Visualize").plotFreqDistr(updatedSuggest)
    importlib.import_module("3-Visualize").plotFreqDistr(updatedDiscard)

    os.rename("cache/suggest.json", "cache/old-suggest.json")
    os.rename("cache/discard.json", "cache/old-discard.json")

    importlib.import_module("1-Scrape").serialize("suggest", updatedSuggest)
    importlib.import_module("1-Scrape").serialize("discard", updatedSuggest)

    print("Post Audit completed, updated suggest.json and discard.json in-place")
    print("saved previous suggest.json and discard.json as old-suggest.json and old-discard.json")
    print("SUCCESS")
