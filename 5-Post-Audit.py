from print_dict import print_dict as prettyPrintMyListOfDicts
from tweeterpy import TweeterPy
import argparse
import importlib

twitter = None
DEBUG = importlib.import_module("1-Scrape").DEBUG
allFollowedUsersSoFar = None


def getNewlyFollowedUsernames(seedUsername):
    preAuditFollowing = set(importlib.import_module("2-Suggest").deserialize("seedsFollowing"))
    postAuditFollowing = set(getFollowingList(seedUsername, shouldSerialize=True, filename="newFollowing"))
    newlyFollowedUsernames = postAuditFollowing.difference(preAuditFollowing)
    if len(newlyFollowedUsernames) == 0:
        print("You are all caught up! No need for a post audit.")
        exit(0)
    global allFollowedUsersSoFar
    allFollowedUsersSoFar = preAuditFollowing.union(postAuditFollowing)
    return newlyFollowedUsernames


def getFollowingList(seedUsername, shouldSerialize=False, filename="", filter=None):
    if shouldSerialize and filename == "":
        while len(filename) == 0:
            filename = input(f"Enter Filename for following list of {seedUsername}")
    alreadyFollowedBySeedUser = list()
    buildDirtySeedListOfDicts = importlib.import_module("1-Scrape").buildDirtySeedListOfDicts
    filterDirtySeedListOfDicts = importlib.import_module("1-Scrape").filterDirtySeedListOfDicts
    for record in sorted(
        filterDirtySeedListOfDicts(buildDirtySeedListOfDicts(seedUsername)),
        key=lambda x: x["followers"],
        reverse=True,
    ):
        if filter == None:
            alreadyFollowedBySeedUser.append(record.get("username"))
        elif record.get("username") not in filter:
            alreadyFollowedBySeedUser.append(record.get("username"))
    if DEBUG:
        print(alreadyFollowedBySeedUser)
    if shouldSerialize:
        importlib.import_module("1-Scrape").serialize(filename, alreadyFollowedBySeedUser)
    return alreadyFollowedBySeedUser


def getFollowerCount(seedUsername):
    return twitter.get_user_info(twitter.get_user_id(seedUsername)).get("legacy", {}).get("followers_count")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process username and password inputs.(Avoid using your primary account)")
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
            "following": getFollowingList(username, filter=allFollowedUsersSoFar),
            "followers": getFollowerCount(username),
        }
        postAuditListOfDicts.append(entry)

    postAuditListOfDicts = sorted(postAuditListOfDicts, key=lambda x: x["followers"], reverse=True)
    importlib.import_module("1-Scrape").serialize("seedDeltaPostAudit", postAuditListOfDicts)
    if DEBUG:
        prettyPrintMyListOfDicts(postAuditListOfDicts)
