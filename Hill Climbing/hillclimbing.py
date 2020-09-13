class ChessBoard:
    def __init__(self, pos, N = 8):
        self.N = N
        self.table = [[0 for i in range(N)] for j in range(N)]
        self.queens = []
        for i in range(0,16,2):
            self.table[pos[i]][pos[i+1]] = 'Q'
            self.queens.append((pos[i], pos[i + 1]))
        self.queens.sort()
        for i in self.table:
            print(i)

    def setPiece (self, row, col):
        self.table[row][col] = 'Q'

    def compute_score (self):
        n_attacked_pieces = 0
        for row in range(self.N):
            for col in range(self.N):
                attacked = False
                for r, c in self.queens:
                    if r == row or c == col or abs(r - row) == abs(c - col):
                        attacked = True
                        break
                if attacked:
                    n_attacked_pieces += 1
        return n_attacked_pieces

    def hillclimbing (self):
        next_state = self.queens
        self.best_next_state = []
        self.best_score = 0
        
        def neightboor(next_state):
            if len(next_state) == self.N:
                self.queens, next_state = next_state, self.queens
                score = self.compute_score()
                if self.best_score < score:
                    score = self.best_score
                    self.best_next_state = next_state
                self.queens, next_state = next_state, self.queens
                return
            row = len(next_state)
            for col in range(self.N):
                next_state.append((row, col))
                neightboor(next_state)
                next_state.pop()

        neightboor([])
        if self.best_score <= self.compute_score():
            return
        self.queens = self.best_next_state
        self.hillclimbing()
