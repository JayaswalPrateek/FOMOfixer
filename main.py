from print_dict import print_dict as prettyPrintMyDict
from tweeterpy import TweeterPy
from tweeterpy import config
import argparse


def setup(username, password):
    twitter = TweeterPy()
    print("PSA: Avoid using your primary account")
    twitter.login(username, password)
    if not twitter.logged_in:
        print("Login Failed!")
        exit(1)
    else:
        prettyPrintMyDict(twitter.me)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process username and password inputs.(Avoid using your primary account)"
    )
    parser.add_argument("--username", type=str, required=True, help="The username")
    parser.add_argument("--password", type=str, required=True, help="The password")
    args = parser.parse_args()
    setup(args.username, args.password)

    print("SUCCESS")
