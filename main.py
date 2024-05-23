from print_dict import print_dict as prettyPrintMyListOfDicts
from tweeterpy import TweeterPy
from tweeterpy import config
import argparse

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
            prettyPrintMyListOfDicts(twitter.me)
        return twitter


def getSeedDB(seedUsername, twitter):
    return cleanSeedListOfDictsToDB(
        preProcessDirtySeedListOfDicts(buildDirtySeedListOfDicts(seedUsername, twitter))
    )


def buildDirtySeedListOfDicts(seedUsername, twitter):
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
    cleanSeedListOfDicts = sorted(
        cleanSeedListOfDicts, key=lambda x: x["followers"], reverse=True
    )
    if not DEBUG:
        prettyPrintMyListOfDicts(cleanSeedListOfDicts)
    alreadyFollowedBySeedUser = set()
    for record in cleanSeedListOfDicts:
        alreadyFollowedBySeedUser.add(record.get("username"))
    if DEBUG:
        print(alreadyFollowedBySeedUser)
    for seedRecord in cleanSeedListOfDicts:
        seedRecordUsername = seedRecord.get("username")
        seedRecord["following"] = filterDirtySeedListOfDicts(
            twitter.get_friends(
                user_id=twitter.get_user_id(seedRecordUsername),
                follower=False,
                following=True,
                mutual_follower=False,
                end_cursor=None,
                total=None,
                pagination=True,
            )
        )
        usernameSet = set()
        for record in seedRecord["following"]:
            if record.get("username") not in alreadyFollowedBySeedUser:
                usernameSet.add(record.get("username"))
        seedRecord["following"] = usernameSet
    if DEBUG:
        prettyPrintMyListOfDicts(cleanSeedListOfDicts)


def filterDirtySeedListOfDicts(dirtySeedListOfDicts):
    cleanSeedListOfDicts = list()
    if "data" in dirtySeedListOfDicts and isinstance(
        dirtySeedListOfDicts["data"], list
    ):
        for record in dirtySeedListOfDicts["data"]:
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
                    prettyPrintMyListOfDicts(new_entry)
                if not new_entry.get("following") == 0:
                    cleanSeedListOfDicts.append(new_entry)
            except AttributeError as e:
                print(f"Error processing record: {e}")
    return cleanSeedListOfDicts


def cleanSeedListOfDictsToDB(cleanSeedListOfDicts):
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
