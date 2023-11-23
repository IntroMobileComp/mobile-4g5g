from helper import *

FILE_DIRECTORY = [
    "gen5data.csv",
    "quiz5G.csv",
]
FILE_SELECTOR = 1

datapoint, timeSeries = inputFrom(FILE_DIRECTORY[FILE_SELECTOR], limit=100)
plotWave(datapoint, timeSeries, panelNumber=0, title="What Receiver get.")
frequency = 1
startPhase = [
    rad(71.640772),
    rad(101.490318),
]
h = Matrix(
    [
        [eulerToComplex(45), eulerToComplex(30) / 2],
        [eulerToComplex(60) / 2, eulerToComplex(45) / 2],
    ]
)
hInv = h.inv()
print(hInv)

complexValues = complexFrom(datapoint, timeSeries, frequency, startPhase)
origComplex = reverseComplex(complexValues, hInv)
origValues = complexToValue(origComplex)
plotWave(origValues, timeSeries, panelNumber=1, title="What Sender actually sent.")
plt.show()
