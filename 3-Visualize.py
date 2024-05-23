import matplotlib.pyplot as plt
import importlib


def plotFreqDistr(listOfDicts):
    frequencies = {key: value for key, value in listOfDicts.items() if key is not None}
    counts = [list(frequencies.values()).count(i) for i in range(2, 26)]
    plt.bar(range(2, 26), counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Count")
    plt.title("Frequency Distribution")
    plt.show()


if __name__ == "__main__":
    plotFreqDistr(importlib.import_module("2-Suggest").deserialize("suggest"))
    plotFreqDistr(importlib.import_module("2-Suggest").deserialize("discard"))
    print("SUCCESS")
