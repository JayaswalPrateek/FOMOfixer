from print_dict import print_dict as prettyPrintMyDict
from tweeterpy import TweeterPy
from tweeterpy import config
import argparse
import sqlite3

DEBUG = True


def setup(username, password):
    if DEBUG:
        return
    twitter = TweeterPy()
    print("PSA: Avoid using your primary account")
    twitter.login(username, password)
    if not twitter.logged_in:
        print("Login Failed!")
        exit(1)
    else:
        prettyPrintMyDict(twitter.me)


def getSeedDB(seedUsername):
    return seedDictToDB(preProcessSeedDict(buildSeedDict(seedUsername)))


def buildSeedDict(seedUsername):
    pass


def preProcessSeedDict(uglySeedDict):
    pass


def seedDictToDB(cleanSeedDict):
    conn = sqlite3.connect("db/seed.db")
    return conn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process username and password inputs.(Avoid using your primary account)"
    )
    parser.add_argument("--username", type=str, required=True, help="The username")
    parser.add_argument("--password", type=str, required=True, help="The password")
    args = parser.parse_args()
    setup(args.username, args.password)

    conn = getSeedDB(input("Enter Seed Username: "))

    conn.close()
    print("SUCCESS")
