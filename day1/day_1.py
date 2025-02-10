l1, l2 = [], []
from collections import Counter

with open('day_1/data_1.txt') as f:
    for line in f:
        l1.append(int(line.split()[0]))
        l2.append(int(line.split()[1]))


def get_similarity_scores(l1, l2):
    total = 0
    l1.sort()
    l2.sort()
    for (a, b) in zip(l1, l2):
        diff = abs(a - b)
        total += diff
    print(total)


total = 0
c1, c2 = Counter(l1), Counter(l2)
n1, n2 = [], []
for (a, b) in zip(l1, l2):
    diff = abs(a * c2[a])
    n1.append(a * c2[a])
    n2.append(b * c1[b])

print(sum(n1))