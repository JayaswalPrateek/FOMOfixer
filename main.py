from print_dict import print_dict as prettyPrintMyDict
from tweeterpy import TweeterPy
from tweeterpy import config
import argparse
import sqlite3

DEBUG = False
SKIP_LOGIN = False


def setup(username, password):
    if SKIP_LOGIN:
        return TweeterPy()
    twitter = TweeterPy()
    print("PSA: Avoid using your primary account")
    twitter.login(username, password)
    if not twitter.logged_in:
        print("Login Failed!")
        exit(1)
    else:
        if DEBUG:
            prettyPrintMyDict(twitter.me)
        return twitter


def getSeedDB(seedUsername, twitter):
    return cleanSeedDictToDB(
        preProcessDirtySeedDict(buildDirtySeedDict(seedUsername, twitter))
    )


def buildDirtySeedDict(seedUsername, twitter):
    dirtySeedDict = twitter.get_friends(
        user_id=twitter.get_user_id(seedUsername),
        follower=False,
        following=True,
        mutual_follower=False,
        end_cursor=None,
        total=None,
        pagination=True,
    )
    if DEBUG:
        prettyPrintMyDict(dirtySeedDict)
    return dirtySeedDict


def preProcessDirtySeedDict(dirtySeedDict):
    cleanSeedDict = filterDirtySeedDict(dirtySeedDict)
    if DEBUG:
        prettyPrintMyDict(cleanSeedDict)


def filterDirtySeedDict(dirtySeedDict):
    cleanSeedDict = list()
    if "data" in dirtySeedDict and isinstance(dirtySeedDict["data"], list):
        for record in dirtySeedDict["data"]:
            try:
                user_data = (
                    record.get("content", {})
                    .get("itemContent", {})
                    .get("user_results", {})
                    .get("result", {})
                    .get("legacy", {})
                )
                new_entry = {
                    "username": user_data.get("screen_name"),
                    "following": user_data.get("friends_count"),
                    "followers": user_data.get("followers_count"),
                }
                if DEBUG:
                    print("new_entry built")
                    prettyPrintMyDict(new_entry)
                if not new_entry.get("following") == 0:
                    cleanSeedDict.append(new_entry)
            except AttributeError as e:
                print(f"Error processing record: {e}")
    return cleanSeedDict


def cleanSeedDictToDB(cleanSeedDict):
    conn = sqlite3.connect("db/seed.db")
    return conn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process username and password inputs.(Avoid using your primary account)"
    )
    parser.add_argument(
        "--username", type=str, required=not SKIP_LOGIN, help="The username"
    )
    parser.add_argument(
        "--password", type=str, required=not SKIP_LOGIN, help="The password"
    )
    args = parser.parse_args()
    twitter = setup(args.username, args.password)

    conn = getSeedDB(input("Enter Seed Username: "), twitter)

    conn.close()
    print("SUCCESS")
