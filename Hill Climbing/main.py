from itertools import groupby
from hillclimbing import ChessBoard

print()
file = open('input.txt')
data = map(lambda el: int(el),file.read().split())
cases, *tail = data
positions = [ tail[i:i+16] for i in range(0,cases*16,16)]
cb = ChessBoard(positions[0])
