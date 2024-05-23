import importlib
import os


if __name__ == "__main__":
    for username in list(importlib.import_module("2-Suggest").deserialize("suggest").keys()):
        os.system(f"xdg-open {"https://x.com/" + username}")
    print("SUCCESS")
