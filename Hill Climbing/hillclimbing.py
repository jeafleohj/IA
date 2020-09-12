class ChessBoard:
    def __init__(self, pos):
        self.table = [[0 for i in range(8)] for j in range(8)]
        for i in range(0,16,2):
            self.table[pos[i]][pos[i+1]] = 'Q'
        for i in self.table:
            print(i)

    def setPiece(self, x,y):
        table[x][y] = 'Q'
