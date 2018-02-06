
MONDAY = 1
TUESDAY = MONDAY << 1

daycodes = 'M T W TH F S SU'.split()
days = range(7)

from itertools import combinations

for idx in range(1, 4):
    for combo in combinations(days, idx):
        print(combo)

print '{0:07b}'.format((1 << 0) + (1 << 1))

