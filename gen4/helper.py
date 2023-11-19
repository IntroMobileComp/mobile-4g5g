from math import cos, sin, pi
from matplotlib import pyplot as plt

fig, grphs = plt.subplots(4, 1)


def classify(datapoint: list[dict[str, float]]) -> list[dict[str, float]]:
    waveList = []
    sampleRate = sampleRateOf(datapoint)
    valueList = map(lambda x: x["value"], datapoint)
    valueList = list(valueList)
    n = len(valueList)
    fLimit = n // 2
    for k in range(fLimit):
        ReBar, ImBar = ReImBar(valueList, k)
        f = k * sampleRate / n
        obj = {}
        obj["f"] = f
        obj["cosAmp"] = ReBar
        obj["sinAmp"] = ImBar
        waveList.append(obj)
    return waveList


def plotDataPoint(datapoint: list[dict[str, float]]) -> None:
    timeSeries = map(lambda x: x["time"], datapoint)
    timeSeries = list(timeSeries)
    valueList = map(lambda x: x["value"], datapoint)
    valueList = list(valueList)
    grphs[0].plot(timeSeries, valueList)


def plotWave(
    waveList: list[dict[str, float]], sampleRate: float, pointNum: int, startAt: float
) -> tuple[list[list[float]], list[list[float]], list[float]]:
    timeDomain = timeSerieFrom(sampleRate, pointNum, startAt)
    cosMatrix = []
    sinMatrix = []
    for wave in waveList:
        f = wave["f"]
        cosAmp = wave["cosAmp"]
        sinAmp = wave["sinAmp"]
        cosDataPoint = genPoint(cosAmp, cos, f, timeDomain)
        sinDataPoint = genPoint(sinAmp, sin, f, timeDomain)
        cosMatrix.append(cosDataPoint)
        sinMatrix.append(sinDataPoint)

        grphs[2].plot(timeDomain, cosDataPoint, label="cos")
        grphs[2].plot(timeDomain, sinDataPoint, label="sin")
    return cosMatrix, sinMatrix, timeDomain


def plotClasifyWave(waveList: list[dict[str, float]]) -> None:
    cosAmpList = map(lambda x: x["cosAmp"], waveList)
    cosAmpList = list(cosAmpList)
    sinAmpList = map(lambda x: x["sinAmp"], waveList)
    sinAmpList = list(sinAmpList)
    fList = map(lambda x: x["f"], waveList)
    fList = list(fList)

    width = 0.25
    x = grphs[1].bar(fList, cosAmpList, width, label="cosAmp")
    grphs[1].bar_label(x, padding=3)

    newFlist = [x + width for x in fList]

    y = grphs[1].bar(newFlist, sinAmpList, width, label="sinAmp")
    grphs[1].bar_label(y)

    grphs[1].legend()


def combineWave(
    cosMatrix: list[list[float]], sinMatrix: list[list[float]]
) -> list[float]:
    combined = []
    for timeUnit in range(len(cosMatrix[0])):
        total = 0
        for rowIdx in range(len(cosMatrix)):
            cosValue = cosMatrix[rowIdx][timeUnit]
            sinValue = sinMatrix[rowIdx][timeUnit]
            total += cosValue + sinValue
        combined.append(total)
    return combined


def ReIm(sample: list[float], k: int) -> tuple[float, float]:
    totalRe = 0.0
    totalIm = 0.0
    n = len(sample)
    for i in range(n):
        cosComp = cos(2 * pi * k * i / n)
        totalRe += sample[i] * cosComp

        sinComp = sin(2 * pi * k * i / n)
        totalIm += sample[i] * sinComp
    return totalRe, -totalIm


def ReImBar(sample: list[float], k: int) -> tuple[float, float]:
    n = len(sample)
    nHalf = n / 2
    Re, Im = ReIm(sample, k)
    ReBar = Re / n if k == 0 or k == n / 2 else Re / nHalf
    ImBar = -Im / nHalf
    return ReBar, ImBar


def genPoint(amp: float, func, freq: float, timeDomain: list[float]) -> list[float]:
    dataPoint = []
    for time in timeDomain:
        funcComp = 2 * pi * freq * time
        funcComp = func(funcComp)
        dataPoint.append(amp * funcComp)
    return dataPoint


def sampleRateOf(datapoint: list[dict[str, float]]) -> float:
    time1 = datapoint[0]["time"]
    time2 = datapoint[1]["time"]
    duration = time2 - time1
    return 1 / duration


def timeSerieFrom(sampleRate: float, pointNum: int, startAt: float) -> list[float]:
    timeDomain = []
    for i in range(pointNum):
        timeDomain.append(startAt + i / sampleRate)
    return timeDomain


def inputFrom(filename: str) -> list[dict[str, float]]:
    datapoint = []
    file = open(filename, "r")
    file.readline()
    for line in file:
        obj = {}
        line = line.strip().split(",")
        obj["time"] = float(line[0])
        obj["value"] = float(line[1])
        datapoint.append(obj)
    file.close()
    return datapoint


"""
filename = "gen4data.csv"
datapoint = inputFrom(filename)[:100]
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
"""
