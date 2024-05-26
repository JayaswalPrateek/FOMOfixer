import importlib
import subprocess
import time

PARTITION_SIZE = 50


def audit(src):
    PARTITIONS = int(len(src) / PARTITION_SIZE) + (len(src) % PARTITION_SIZE > 0)
    print(f"PARTITION_SIZE = {PARTITION_SIZE}")
    print(f"PARTITIONS = {PARTITIONS}")
    partitionNumber = int(input("Enter Partition Number: "))
    if partitionNumber <= 0 or partitionNumber > PARTITIONS:
        print(f"Invalid input: Valid values in range [1,{PARTITIONS}]")
        exit(1)
    start = (partitionNumber - 1) * PARTITION_SIZE
    end = start + PARTITION_SIZE
    if end > len(src):
        end = len(src)
    for username in src[start:end]:
        subprocess.run(["xdg-open", f"https://x.com/{username}"], check=True)
        time.sleep(0.5)


if __name__ == "__main__":
    audit(list(importlib.import_module("2-Suggest").deserialize("suggest").keys()))
    print("SUCCESS")
