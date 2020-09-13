from sys import setrecursionlimit
from hillclimbing import ChessBoard
import timeit
from sys import stdout

setrecursionlimit(int(1e9))
N = 8
queens = []
score = dict()
max_time = 0
it = 0
total = N**N

def backtrack ():
    global max_time
    global it
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
        it += 1
        stdout.write('Process = %.2f%%  \r' %(100.0 * it / total))
        stdout.flush()
        return
    for r in range(N):
        queens.append(r)
        backtrack()
        queens.pop()
backtrack()
with open('data.txt', 'w') as file:
    file.write('Max_time: %.6f mili seconds\n' %(max_time))
    for score, frecuency in score.items():
        file.write('%d %d\n' %(score, frecuency))
