DEBUG = False
CACHE_DIR_NAME = "cache"


def deserialize(fileName):
    filePath = f"{CACHE_DIR_NAME}/{fileName}.json"
    if not os.path.exists(filePath):
        if DEBUG:
            print(f"File '{filePath}' does not exist.")
        return None
    with open(filePath, "r") as json_file:
        data = json.load(json_file)
        if DEBUG:
            print(f"Data successfully read from '{filePath}'.")
        return data
