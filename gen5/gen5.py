from helper import *

FILE_DIRECTORY = [
    "gen5data.csv",
    ".csv",
]
FILE_SELECTOR = 0

datapoint, timeSeries = inputFrom(FILE_DIRECTORY[FILE_SELECTOR], limit=100)
plotWave(datapoint, timeSeries, panelNumber=0, title="What Receiver get.")
frequency = 1
startPhase = [
    rad(71.640772),
    rad(101.490318),
]
h = Matrix(
    [
        [simplify("1/2"), simplify("I/3")],
        [simplify("I/4"), simplify("1/6")],
    ]
)
hInv = h.inv()

complexValues = complexFrom(datapoint, timeSeries, frequency, startPhase)
origComplex = reverseComplex(complexValues, hInv)
origValues = complexToValue(origComplex)
plotWave(origValues, timeSeries, panelNumber=1, title="What Sender actually sent.")
plt.show()
