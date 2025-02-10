from typing import List

data = open("day_2/data_2.txt")



def check_report(l: List[int]) -> bool:
    min_diff, max_diff = 1, 3
    i = 0
    decrease = ((l[0] - l[1]) > 0)

    i = 0
    good = True
    while good:
        if decrease:
            if l[i] > l[i + 1]:
                good = True
            else:
                return False
        else:
            if l[i] < l[i + 1]:
                good = True
            else:
                return False

        if min_diff <= abs(l[i] - l[i + 1]) <= max_diff:
            i += 1
            if i == len(l) - 1:
                return True
        else:
            return False
        

total = 0
unsafe_reports = []
for line in data:
    l = [int(j) for j in line.split(" ")]
    if check_report(l):
        total += 1
    else:
        unsafe_reports.append(l)

print(total)
for unsafe_report in unsafe_reports:
    for i in range(len(unsafe_report)):
        t = unsafe_report[:i] + unsafe_report[i + 1:]
        if check_report(t):
            print(f"NEW SAFE: {t}")
            total += 1
            break
        

print(total)






