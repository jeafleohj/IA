from sys import exit
from hillclimbing import ChessBoard

with open('input.txt') as file:
    grid = []
    for line in file:
        row = list(map(int, line.split()))
        grid.append(row)
    N = len(grid)
    for row in grid:
        if len(row) != N:
            print('Matrix is invalid')
            exit(-1)
    queens = []
    for c in range(N):
        row, cnt = -1, 0
        for r in range(N):
            if grid[r][c] == 1:
                row = r
                cnt += 1
        if cnt != 1:
            print('Matrix is invalid')
            exit(-1)
        queens.append(row)
    chess = ChessBoard(queens)
    chess.hillclimbing()
    print(chess.get_table())
    print(chess.get_score())
