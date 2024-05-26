import importlib
import matplotlib.pyplot as plt


def plotFreqDistr(listOfDicts):
    frequencies = {key: value for key, value in listOfDicts.items() if key is not None}
    minFreq = min(frequencies.values())
    maxFreq = max(frequencies.values())
    counts = [list(frequencies.values()).count(i) for i in range(minFreq, maxFreq + 1)]
    plt.bar(range(minFreq, maxFreq + 1), counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Count")
    plt.title("Frequency Distribution")
    plt.show()


if __name__ == "__main__":
    plotFreqDistr(importlib.import_module("2-Suggest").deserialize("suggest"))
    plotFreqDistr(importlib.import_module("2-Suggest").deserialize("discard"))
    print("SUCCESS")
