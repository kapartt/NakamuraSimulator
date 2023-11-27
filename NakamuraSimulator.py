from random import random
from itertools import accumulate

gamesCount = 600
simulationsCount = 1000
pointsFracThreshold = 0.985
minSeriesLen = 35
maxSeriesLen = 100

winProb = 0.88
drawProb = 0.04
loseProb = 1 - winProb - drawProb

seriesSum = 0


def getRes(x, w, d):
    if x < w:
        return 1
    
    if x < w + d:
        return 0.5
    
    return 0


nakaSeriesCountOnSimulation = {}

for simulationIndex in range(simulationsCount):
    streakLen = 0
    streakPts = 0.0
    nakaSeriesCount = 0
    sumGamesOnStreaks = 0
    
    results = [0] + [getRes(random(), winProb, drawProb) for _ in range(gamesCount)]
    prefixSums = list(accumulate(results))
    
    print('Simulation #', (simulationIndex + 1))
    
    gameIndex = 0
    
    while gameIndex < gamesCount - minSeriesLen:
        f = False
        successSeriesLen = 0   
        successPts = 0
        newMaxSeriesLen = min(maxSeriesLen, gamesCount - gameIndex)
        
        for seriesLen in range(minSeriesLen, newMaxSeriesLen):            
            streakPts = prefixSums[gameIndex + seriesLen] - prefixSums[gameIndex]
            
            if streakPts / seriesLen >= pointsFracThreshold:
                f = True
                print('StreakLen = ', seriesLen, ', StreakPts = ', streakPts, ', from game #', (gameIndex + 1), sep='')
                sumGamesOnStreaks += seriesLen
                break
        if f:
            nakaSeriesCount += 1
            gameIndex += seriesLen
        else:
            gameIndex += 1
            
    print('NakaSeriesCount =', nakaSeriesCount)
    seriesSum += nakaSeriesCount
    
    v = nakaSeriesCountOnSimulation.get(nakaSeriesCount, 0)
    nakaSeriesCountOnSimulation[nakaSeriesCount] = v + 1
    
    print('PtsFraction =', sum(results) / gamesCount)
    print()
    
print('Average streaks count =', seriesSum / simulationsCount)
            
for x in sorted(nakaSeriesCountOnSimulation):
    simStr = "simulation" if nakaSeriesCountOnSimulation[x] == 1 else "simulations"
    print('{0} {1} ({2:.1%}) with {3} streaks'.format(nakaSeriesCountOnSimulation[x], simStr, nakaSeriesCountOnSimulation[x] / simulationsCount, x))
