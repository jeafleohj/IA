from math import inf as INF

class ChessBoard:
    def __init__ (self, queens):
        self.N = len(queens)
        self.queens = queens

    def get_table (self):
        table = [[0 for i in range(self.N)] for j in range(self.N)]
        for c in range(self.N):
            r = self.queens[c]
            table[r][c] = 1
        return "\n".join(' '.join(str(c) for c in row) for row in table)

    def get_score (self):
        return self.compute_score(self.queens)

    def compute_score (self, state):
        score = 0
        for c1 in range(self.N):
            r1 = self.queens[c1]
            for c2 in range(c1 + 1, self.N):
                r2 = self.queens[c2]
                if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                    score += 1
        return score


    def hillclimbing (self):
        while True:
            best_next_state = []
            best_score = INF
            for c in range(self.N):
                prev = self.queens[c]
                for r in range(self.N):
                    if r == prev:
                        continue
                    self.queens[c] = r
                    score = self.compute_score(self.queens)
                    if score < best_score:
                        best_score = score
                        best_next_state = [r for r in self.queens]
                self.queens[c] = prev    
    
            if best_score >= self.compute_score(self.queens):
                break
            self.queens = best_next_state
