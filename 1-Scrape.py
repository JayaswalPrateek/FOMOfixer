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
    twitter = TweeterPy()
    print("PSA: Avoid using your primary account")
    twitter.login(username, password)
    if not twitter.logged_in:
        print("Login Failed!")
        exit(1)
    else:
        if DEBUG:
            prettyPrintMyListOfDicts(twitter.me)


def serialize(fileName, listOfDicts):
    if not os.path.exists(CACHE_DIR_NAME):
        os.makedirs(CACHE_DIR_NAME)
        if DEBUG:
            print(f"Directory '{CACHE_DIR_NAME}' created successfully.")
    elif DEBUG:
        print(f"Directory '{CACHE_DIR_NAME}' already exists.")
    json_string = json.dumps(listOfDicts, indent=4)
    with open(f"{CACHE_DIR_NAME}/{fileName}.json", "w") as json_file:
        json_file.write(json_string)
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
    cleanSeedListOfDicts = filterDirtySeedListOfDicts(dirtySeedListOfDicts)
    cleanSeedListOfDicts = sorted(cleanSeedListOfDicts, key=lambda x: x["followers"], reverse=True)
    if DEBUG:
        prettyPrintMyListOfDicts(cleanSeedListOfDicts)
    alreadyFollowedBySeedUser = list()
    for record in cleanSeedListOfDicts:
        alreadyFollowedBySeedUser.append(record.get("username"))
    if DEBUG:
        print(alreadyFollowedBySeedUser)
    serialize("seedsFollowing", alreadyFollowedBySeedUser)
    for seedRecord in cleanSeedListOfDicts:
        seedRecordUsername = seedRecord.get("username")
        seedRecord["following"] = filterDirtySeedListOfDicts(buildDirtySeedListOfDicts(seedRecordUsername))
        usernameSet = list()
        for record in seedRecord["following"]:
            if record.get("username") not in alreadyFollowedBySeedUser:
                usernameSet.append(record.get("username"))
        seedRecord["following"] = usernameSet
    if DEBUG:
        prettyPrintMyListOfDicts(cleanSeedListOfDicts)
    serialize("seed", cleanSeedListOfDicts)


def filterDirtySeedListOfDicts(dirtySeedListOfDicts):
    cleanSeedListOfDicts = list()
    for record in dirtySeedListOfDicts["data"]:
        try:
            user_data = record.get("content", {}).get("itemContent", {}).get("user_results", {}).get("result", {}).get("legacy", {})
            new_entry = {
                "username": user_data.get("screen_name"),
                "following": user_data.get("friends_count"),
                "followers": user_data.get("followers_count"),
            }
            if DEBUG:
                print("new_entry built")
                prettyPrintMyListOfDicts(new_entry)
            cleanSeedListOfDicts.append(new_entry)
        except AttributeError as e:
            print(f"Error processing record: {e}")
    return cleanSeedListOfDicts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process username and password inputs.(Avoid using your primary account)")
    parser.add_argument("--username", type=str, required=not SKIP_LOGIN, help="The username")
    parser.add_argument("--password", type=str, required=not SKIP_LOGIN, help="The password")
    args = parser.parse_args()
    setup(args.username, args.password)
    buildSeedJson(input("Enter Seed Username: "))
    print("SUCCESS")
