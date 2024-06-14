from collections import Counter
from print_dict import print_dict as prettyPrintMyListOfDicts
from tweeterpy import TweeterPy
import argparse
import importlib
import os

twitter = None
DEBUG = importlib.import_module("1-Scrape").DEBUG
SUGGESTION_THRESHOLD = importlib.import_module("2-Suggest").SUGGESTION_THRESHOLD
everyUserFollowedBySeedUserSoFar = None


def getNewlyFollowedUsernames(seedUsername):
    preAuditFollowing = set(importlib.import_module("2-Suggest").deserialize("seedsFollowing"))
    postAuditFollowing = set(getFollowingList(seedUsername, shouldSerialize=True, filename="newFollowing"))
    newlyFollowedUsernames = postAuditFollowing.difference(preAuditFollowing)
    if len(newlyFollowedUsernames) == 0:
        print("You are all caught up! No need for a post audit.")
        exit(0)
    global everyUserFollowedBySeedUserSoFar
    everyUserFollowedBySeedUserSoFar = preAuditFollowing.union(postAuditFollowing)  # includes both: newly followed/unfollowed usernames
    return newlyFollowedUsernames


def getFollowingList(seedUsername, shouldSerialize=False, filename="", filter=None):
    if shouldSerialize and filename == "":
        while len(filename) == 0:
            filename = input(f"Enter Filename for following list of {seedUsername}")
    followedBySeedUser = list()
    buildDirtySeedListOfDicts = importlib.import_module("1-Scrape").buildDirtySeedListOfDicts
    filterDirtySeedListOfDicts = importlib.import_module("1-Scrape").filterDirtySeedListOfDicts
    for record in sorted(
        filterDirtySeedListOfDicts(buildDirtySeedListOfDicts(seedUsername)),
        key=lambda x: x["followers"],
        reverse=True,
    ):
        if filter == None:
            followedBySeedUser.append(record["username"])
        elif record["username"] not in filter:
            followedBySeedUser.append(record["username"])
    if DEBUG:
        print(followedBySeedUser)
    if shouldSerialize:
        importlib.import_module("1-Scrape").serialize(filename, followedBySeedUser)
    return followedBySeedUser


def getFollowerCount(seedUsername):
    return twitter.get_user_info(twitter.get_user_id(seedUsername)).get("legacy", {}).get("followers_count")


def sortSeedsFollowingByTheirFollowingCount(seedUsername, serialize=False):
    resultKeys = getFollowingList(seedUsername)
    resultValues = list()
    for username in resultKeys:
        entry = twitter.get_user_info(twitter.get_user_id(username)).get("legacy", {}).get("friends_count", {})
        resultValues.append(entry)
    result = dict(zip(resultKeys, resultValues))
    sortedResult = dict(sorted(result.items(), key=lambda item: item[1]))
    if serialize:
        importlib.import_module("1-Scrape").serialize("seedsFollowingSortedByFollowingCount", sortedResult)
    if DEBUG:
        prettyPrintMyListOfDicts(sortedResult)
    return sortedResult


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process username and password inputs.")
    parser.add_argument("--username", type=str, required=True, help="The username")
    parser.add_argument("--password", type=str, required=True, help="The password")
    args = parser.parse_args()
    importlib.import_module("1-Scrape").setup(args.username, args.password)
    twitter = importlib.import_module("1-Scrape").twitter

    newAlreadyFollowing = getNewlyFollowedUsernames(seedUsername=input("Enter Seed Username: "))
    postAuditListOfDicts = list()
    for username in newAlreadyFollowing:
        entry = {
            "username": username,
            "following": getFollowingList(username, filter=everyUserFollowedBySeedUserSoFar),
            "followers": getFollowerCount(username),
        }
        postAuditListOfDicts.append(entry)

    postAuditListOfDicts = sorted(postAuditListOfDicts, key=lambda x: x["followers"], reverse=True)
    importlib.import_module("1-Scrape").serialize("seedDeltaPostAudit", postAuditListOfDicts)
    if DEBUG:
        prettyPrintMyListOfDicts(postAuditListOfDicts)

    print("SUCCESS")
