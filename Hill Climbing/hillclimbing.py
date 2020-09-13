class ChessBoard:
    def __init__ (self, queens):
        self.N = len(queens)
        self.queens = queens

    def get_table (self):
        table = [[0 for i in range(self.N)] for j in range(self.N)]
        for c in range(self.N):
            r = self.queens[c]
            table[r][c] = 1
        return "\n".join(''.join(str(c) for c in row) for row in table)

    def get_score (self):
        return self.compute_score(self.queens)

    def compute_score (self, state):
        n_non_attacked_pieces = 0
        for row in range(self.N):
            for col in range(self.N):
                attacked = False
                for c in range(self.N):
                    r = state[c]
                    if r == row or abs(r - row) == abs(c - col):
                        attacked = True
                        break
                if not attacked:
                    n_non_attacked_pieces += 1
        return n_non_attacked_pieces

    def hillclimbing (self):
        best_next_state = []
        best_score = 0
        
        for c in range(self.N):
            prev = self.queens[c]
            for r in range(self.N):
                if r == prev:
                    continue
                self.queens[c] = r
                score = self.compute_score(self.queens)
                if best_score < score:
                    best_score = score
                    best_next_state = [r for r in self.queens]
            self.queens[c] = prev
        
        if best_score <= self.compute_score(self.queens):
            return
        self.queens = best_next_state
        self.hillclimbing()
