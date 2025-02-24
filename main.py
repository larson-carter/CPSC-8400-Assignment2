import os, sys, math, random
from functools import cmp_to_key

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped
try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

N = 0  # problem size

def mycomp(p1, p2, v):
    return grader.compare(p1, p2, v)
    #return compare_local(p1, p2, v)

def compare_local(player1, player2, v):
    global N
    if player1 < 0 or player1 >= N:
        print('Invalid value of player1!')
        sys.exit(0)
    if player2 < 0 or player2 >= N:
        print('Invalid value of player2!')
        sys.exit(0)
    if v < 0 or v > 1:
        print('Invalid value of v!')
        sys.exit(0)

    peak1 = 1.0 - (1.0 + player1) / (1.0 + N)
    peak2 = 1.0 - (1.0 + player2) / (1.0 + N)
    c1 = math.sqrt(v * peak1) if v <= peak1 else 1 - math.sqrt((1 - v) * (1 - peak1))
    c2 = math.sqrt(v * peak2) if v <= peak2 else 1 - math.sqrt((1 - v) * (1 - peak2))
    return -1 if c1 <= c2 else 1

class FairDivisionSolver:
    def __init__(self, n, compareFunc):
        self.n = n
        self.compareFunc = compareFunc

    def myComp(self, p1, p2, v):
        return self.compareFunc(p1, p2, v)

    def divList(self, arr, left, right, pIndex, v):
        pivot = arr[pIndex]
        arr[pIndex], arr[right] = arr[right], arr[pIndex]
        startIndex = left
        for i in range(left, right):
            if self.myComp(arr[i], pivot, v) <= 0:
                arr[startIndex], arr[i] = arr[i], arr[startIndex]
                startIndex += 1
        arr[right], arr[startIndex] = arr[startIndex], arr[right]
        return startIndex

    def qSelect(self, arr, left, right, k, v):
        if left == right:
            return
        pIndex = random.randint(left, right)
        pIndex = self.divList(arr, left, right, pIndex, v)
        if k == pIndex:
            return
        elif k < pIndex:
            self.qSelect(arr, left, pIndex - 1, k, v)
        else:
            self.qSelect(arr, pIndex + 1, right, k, v)

    def divSplitOrder(self, players, vHalf):
        if len(players) <= 1:
            return players
        if len(players) % 2 == 0:
            k = len(players) // 2
            dupPlayers = list(players)
            self.qSelect(dupPlayers, 0, len(dupPlayers) - 1, k, vHalf / 2)
            leftSplit = dupPlayers[:k]
            rightSplit = dupPlayers[k:]
            leftOrder = self.divSplitOrder(leftSplit, vHalf / 2)
            rightOrder = self.divSplitOrder(rightSplit, vHalf / 2)
            return leftOrder + rightOrder
        else:
            minPlayer = players[0]
            for p in players[1:]:
                if self.myComp(p, minPlayer, vHalf / len(players)) < 0:
                    minPlayer = p
            leftOverValue = [p for p in players if p != minPlayer]
            return [minPlayer] + self.divSplitOrder(leftOverValue, vHalf)

    def Solve(self, players, vHalf=1.0):
        return self.divSplitOrder(players, vHalf)

def main():
    global N
    try:
        N = int(os.environ["N"])
    except:
        # Testing values; you can adjust for local testing.
        N = 21
        # N = 30
        # N = 15
        # N = 7

    players = list(range(N))
    solver = FairDivisionSolver(N, mycomp)
    ordering = solver.Solve(players, 1.0)

    print('\n'.join(str(player) for player in ordering))

if __name__ == "__main__":
    main()
