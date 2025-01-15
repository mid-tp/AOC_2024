from typing import List, Tuple

data = open("day_5/data_5.txt")

rules = dict()

first_part = True
UPDATES = []
for line in data:
    if line == "\n":
        first_part = False
        continue
    if first_part:
        p1, p2 = line.strip().split("|")
        p1, p2 = int(p1), int(p2)
        if p1 in rules.keys():
            rules[p1].append(p2)
        else:
            rules[p1] = [p2]
    else:
        l = []
        for i in line.strip().split(","):
            l.append(int(i))
        UPDATES.append(l)

# print(rules) # meaning that if key -> value, that key should be before value
# print(updates)
    

# updates = [[75,97,47,61,53]]

def get_middle(l: List[int]) -> int:
    return l[len(l) // 2]

def get_good_bad_updates(l_updates: List[List[int]]) -> Tuple[List[int], List[int]]:
    good_updates = []
    bad_updates = []
    for update in l_updates:
        good = True
        for i in range(len(update)):
            for j in update[i + 1:]:
                if j not in rules.keys():
                    continue
                if update[i] in rules[j]:
                    good = False
                    break
                break
        if good:
            good_updates.append(update)
        else:
            bad_updates.append(update)
    
    return good_updates, bad_updates


good_updates_1, bad_updates_1 = get_good_bad_updates(UPDATES)

total = 0
for l in good_updates_1:
    total += get_middle(l)

print(total)


# change the order 

def fix_bad_updates(bad_updates: List[List[int]]) -> List[List[int]]:
    fixed_updates = []
    # print(f"We loop over {bad_updates}")
    for bad_update in bad_updates:
        fixed = False
        # print(f"update: {bad_update}\n")
        bad_update_cp = bad_update[::]
        for i in range(len(bad_update)):
            for j in range(len(bad_update[i + 1:])):
                if bad_update[i + j + 1] not in rules.keys():
                    continue
                if bad_update[i] in rules[bad_update[i + j + 1]]:
                    # print(f"we need to swap {bad_update[i]} and {bad_update[i + j + 1]}")
                    cp_i = bad_update_cp[i]
                    bad_update_cp[i] = bad_update[i + j + 1]
                    bad_update_cp[i + j + 1] = cp_i
                    fixed_updates.append(bad_update_cp)   
                    fixed = True
                    break
            if fixed:
                break
    return fixed_updates


great_updates = []

while len(bad_updates_1) > 0:
    print("------------------------------------")
    fixed_updates = fix_bad_updates(bad_updates_1)
    print(f"\nfixed updates: {fixed_updates}")
    # Check if the updates are actually fixed
    good_updates, bad_updates_1 = get_good_bad_updates(fixed_updates)
    print(f"(AFTER FIX) The good updates: {good_updates}\n")
    print(f"(AFTER FIX) The bad updates: {bad_updates_1}\n")
    if len(good_updates) == 0:
        continue
    for gu in good_updates:
        great_updates.append(gu)
    

print(great_updates)

total = 0
for l in great_updates:
    total += get_middle(l)
    print(f"+{get_middle(l)}")

print(total)
