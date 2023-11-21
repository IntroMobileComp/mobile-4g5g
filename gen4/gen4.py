from helper import *

FILE_DIRECTORY = [
    "gen4data.csv",
    "Quiz4g.csv",
]
FILE_SELECTOR = 1

datapoint = inputFrom(FILE_DIRECTORY[FILE_SELECTOR])[:100]
plotDataPoint(datapoint)
waveList = classify(datapoint)
plotClasifyWave(waveList)
pointNum = len(datapoint)
sampleRate = sampleRateOf(datapoint)
startAt = min(datapoint, key=lambda x: x["time"])["time"]
cosMatrix, sinMatrix, timeDomain = plotWave(waveList, sampleRate, pointNum, startAt)
combinedWave = combineWave(cosMatrix, sinMatrix)
grphs[3].plot(timeDomain, combinedWave)
plt.show()
