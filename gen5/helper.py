from sympy import (
    I,
    Expr,
    SparseMatrix,
    cos,
    im,
    simplify,
    Matrix,
    rad,
    pi,
    sin,
)
from matplotlib import pyplot as plt

fig, gPanel = plt.subplots(2, 1)


def reverseComplex(
    complexValues: list[list[Expr]], hInv: SparseMatrix
) -> list[list[Expr]]:
    reverseValues = [[] for x in range(len(complexValues))]
    for i in range(len(complexValues[0])):
        vector = []
        for complexList in complexValues:
            vector.append([complexList[i]])
        vector = Matrix(vector)
        reverseVector = hInv * vector
        for j in range(len(complexValues)):
            reverseValues[j].append(simplify(reverseVector[j, 0]))
    return reverseValues


def complexToValue(complexMatrix: list[list[Expr]]) -> list[list[float]]:
    valueMatrix = []
    for i in range(len(complexMatrix)):
        complexList = complexMatrix[i]
        valueMatrix.append([])
        for j in range(len(complexList)):
            complexValue = complexList[j]
            imPart = im(complexValue)
            valueMatrix[i].append(imPart)
    return valueMatrix


def complexFrom(
    datapoint: list[list[float]],
    timeSeries: list[float],
    frequency: float,
    startPhase: list[float],
) -> list[list[Expr]]:
    complexValues = []
    startTime = min(timeSeries)
    amps = ampFrom(datapoint)
    for i in range(len(datapoint)):
        complexValues.append([])
        for time in timeSeries:
            complexValue = (
                complexNow(time, startTime, frequency, startPhase[i]) * amps[i]
            )
            complexValues[i].append(complexValue)
    return complexValues


def ampFrom(datapoint: list[list[float]]) -> list[float]:
    amps = []
    for valueList in datapoint:
        maxAmp = max(valueList)
        minAmp = min(valueList)
        avgAmp = (maxAmp - minAmp) / 2
        amps.append(avgAmp)
    return amps


def complexNow(
    timeNow: float, startTime: float, frequency: float, startPhase: float
) -> float:
    timeDiff = timeNow - startTime
    phase = phaseNow(timeNow, startTime, frequency, startPhase)
    return cos(phase) + I * sin(phase)


def phaseNow(
    timeNow: float, startTime: float, frequency: float, startPhase: float
) -> float:
    timeDiff = timeNow - startTime
    phase = 2 * pi * timeDiff * frequency + startPhase
    return float(phase)


def plotWave(
    datapoint: list[list[float]], timeSeries: list[float], panelNumber: int, title: str
) -> None:
    # gPanel[panelNumber].set_xlabel("Time")
    gPanel[panelNumber].set_ylabel("Value")
    gPanel[panelNumber].set_title(title)
    for i in range(len(datapoint)):
        valueList = datapoint[i]
        maxValue = max(valueList)
        minValue = min(valueList)
        gPanel[panelNumber].plot(timeSeries, valueList, label=f"Sender/Receiver[{i}]")
        gPanel[panelNumber].axhline(
            y=maxValue, color="red", linestyle="--", label=f"max[{i}]: {maxValue}"
        )
    gPanel[panelNumber].legend()


def inputFrom(filename: str, limit: int) -> tuple[list[list[float]], list[float]]:
    timeSeries = []
    file = open(filename, "r")
    header = file.readline().split(",")[1:]
    datapoint = [[] for x in range(len(header))]
    for i in range(limit):
        line = file.readline()
        line = line.strip().split(",")
        time = float(line.pop(0))
        timeSeries.append(time)
        line = map(float, line)
        line = list(line)
        for i in range(len(line)):
            datapoint[i].append(line[i])
    return datapoint, timeSeries


# datapoint, timeSeries = inputFrom("gen5data.csv", limit=100)
# plotWave(datapoint, timeSeries, panelNumber=0, title="What Receiver get.")
# frequency = 1
# startPhase = [
#     rad(71.640772),
#     rad(101.490318),
# ]
# h = Matrix(
#     [
#         [simplify("1/2"), simplify("I/3")],
#         [simplify("I/4"), simplify("1/6")],
#     ]
# )
# hInv = h.inv()

# complexValues = complexFrom(datapoint, timeSeries, frequency, startPhase)
# origComplex = reverseComplex(complexValues, hInv)
# origValues = complexToValue(origComplex)
# plotWave(origValues, timeSeries, panelNumber=1, title="What Sender actually sent.")
# plt.show()
