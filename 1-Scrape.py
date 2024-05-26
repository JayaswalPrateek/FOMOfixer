from print_dict import print_dict as prettyPrintMyListOfDicts
from tweeterpy import TweeterPy
from tweeterpy import config
import argparse
import json
import os

twitter = None
DEBUG = False
SKIP_LOGIN = False
CACHE_DIR_NAME = "cache"


def setup(username, password):
    global twitter
    if SKIP_LOGIN:
        twitter = TweeterPy()
        return
    twitter = TweeterPy()
    twitter.login(username, password)
    if not twitter.logged_in:
        print("Login Failed!")
        exit(1)
    else:
        if DEBUG:
            prettyPrintMyListOfDicts(twitter.me)


def serialize(fileName, data):
    if not os.path.exists(CACHE_DIR_NAME):
        os.makedirs(CACHE_DIR_NAME)
        if DEBUG:
            print(f"Directory '{CACHE_DIR_NAME}' created successfully.")
    elif DEBUG:
        print(f"Directory '{CACHE_DIR_NAME}' already exists.")
    jsonString = json.dumps(data, indent=4)
    with open(f"{CACHE_DIR_NAME}/{fileName}.json", "w") as jsonFile:
        jsonFile.write(jsonString)
        if DEBUG:
            print(f"Data successfully written to '{CACHE_DIR_NAME}/{fileName}.json'.")


def buildSeedJson(seedUsername):
    return preProcessDirtySeedListOfDicts(buildDirtySeedListOfDicts(seedUsername))


def buildDirtySeedListOfDicts(seedUsername):
    dirtySeedListOfDicts = twitter.get_friends(
        user_id=twitter.get_user_id(seedUsername),
        follower=False,
        following=True,
        mutual_follower=False,
        end_cursor=None,
        total=None,
        pagination=True,
    )
    if DEBUG:
        prettyPrintMyListOfDicts(dirtySeedListOfDicts)
    return dirtySeedListOfDicts


def preProcessDirtySeedListOfDicts(dirtySeedListOfDicts):
    cleanSeedListOfDicts = sorted(filterDirtySeedListOfDicts(dirtySeedListOfDicts), key=lambda x: x["followers"], reverse=True)
    if DEBUG:
        prettyPrintMyListOfDicts(cleanSeedListOfDicts)
    alreadyFollowedBySeedUser = list()
    for record in cleanSeedListOfDicts:
        alreadyFollowedBySeedUser.append(record["username"])
    if DEBUG:
        print(alreadyFollowedBySeedUser)
    serialize("seedsFollowing", alreadyFollowedBySeedUser)
    for seedRecord in cleanSeedListOfDicts:
        seedRecordUsername = seedRecord["username"]
        seedRecord["following"] = filterDirtySeedListOfDicts(buildDirtySeedListOfDicts(seedRecordUsername))
        usernameList = list()
        for record in seedRecord["following"]:
            if record["username"] not in alreadyFollowedBySeedUser:
                usernameList.append(record["username"])
        seedRecord["following"] = usernameList
    if DEBUG:
        prettyPrintMyListOfDicts(cleanSeedListOfDicts)
    serialize("seed", cleanSeedListOfDicts)


def filterDirtySeedListOfDicts(dirtySeedListOfDicts):
    cleanSeedListOfDicts = list()
    for record in dirtySeedListOfDicts["data"]:
        try:
            data = record.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {}).get("legacy", {})
            entry = {
                "username": data["screen_name"],
                "following": data["friends_count"],
                "followers": data["followers_count"],
            }
            if DEBUG:
                print("built entry:")
                prettyPrintMyListOfDicts(entry)
            cleanSeedListOfDicts.append(entry)
        except AttributeError as e:
            print(f"Error processing record: {e}")
            exit(1)
    return cleanSeedListOfDicts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process username and password inputs.")
    parser.add_argument("--username", type=str, required=not SKIP_LOGIN, help="The username")
    parser.add_argument("--password", type=str, required=not SKIP_LOGIN, help="The password")
    args = parser.parse_args()
    setup(args.username, args.password)
    buildSeedJson(input("Enter Seed Username: "))
    print("SUCCESS")
