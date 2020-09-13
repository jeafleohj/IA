from sys import setrecursionlimit
from hillclimbing import ChessBoard
import timeit

setrecursionlimit(int(1e9))
N = 8
queens = []
score = dict()
max_time = 0

def backtrack ():
    global max_time
    if len(queens) == N:
        chess = ChessBoard(queens)
        chess.hillclimbing()
        start = timeit.default_timer()
        cur_score = chess.get_score()
        stop = timeit.default_timer()
        max_time = max(max_time, 1000 * (stop - start))
        if cur_score not in score:
            score[cur_score] = 1
        else:
            score[cur_score] += 1
        return
    for r in range(N):
        queens.append(r)
        backtrack()
        queens.pop()
backtrack()
print("Max_time: %.6f" %(max_time))
for score, frecuency in score.items():
    print(score, frecuency)
