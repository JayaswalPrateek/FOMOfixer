from print_dict import print_dict as prettyPrintMyDict
from tweeterpy import TweeterPy
from tweeterpy import config
import argparse
import sqlite3

DEBUG = True
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
        prettyPrintMyDict(twitter.me)
        return twitter


def getSeedDB(seedUsername, twitter):
    return seedDictToDB(preProcessSeedDict(buildSeedDict(seedUsername, twitter)))


def buildSeedDict(seedUsername, twitter):
    pass


def preProcessSeedDict(dirtySeedDict):
    pass


def seedDictToDB(cleanSeedDict):
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
