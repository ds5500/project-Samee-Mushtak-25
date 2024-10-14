import random

with open('haloVolc1-merged.fa') as f:
    list = [trna.strip() for trna in f]

primordial = list[:2]
extant = list[2:]
random.shuffle(extant)

for trna in primordial:
    print(trna)
for trna in extant:
    print(trna)
