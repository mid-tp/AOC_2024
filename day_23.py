from typing import List
from collections import defaultdict

from time import time as time


def part1():
    # Read in the data and parse
    data = open("day_23/data_23.txt")
    computer_links = defaultdict(lambda: [])
    pair_set = set()
    unique_computers = set()
    for line in data:

        c1, c2 = line.strip().split("-")
        # Add the pairs to the sets of pairs 
        # We add them in both orders. 
        pair_set.add(frozenset({c1, c2}))
        computer_links[c1].append(c2)
        computer_links[c2].append(c1)

        unique_computers.add(c1)
        unique_computers.add(c2)
    
    # Do a second loop over the data
    triplets = set()
    data = open("day_23/data_23.txt")
    for line in data:
        c1, c2 = line.strip().split("-")
        c1_links = computer_links[c1]
        for i in range(len(c1_links) - 1):
            for j in range(i + 1, len(c1_links)):
                new1, new2 = c1_links[i], c1_links[j]
                s = {new1, new2}
                if s not in pair_set: continue
                triplets.add(frozenset({c1, new1, new2}))
    # print(f"All the triplets:")
    total = 0
    for triplet in triplets:
        c1, c2, c3 = triplet
        if not c1.startswith("t") and not c2.startswith("t") and not c3.startswith("t"): continue
        total += 1
    print(total)


def check_if_cc(cc_potential, pair_set) -> bool:
    cc_potential = list(cc_potential)
    for i in range(len(cc_potential) - 1):
        for j in range(i + 1, len(cc_potential)):
            if {cc_potential[i], cc_potential[j]} not in pair_set:
                return False
    return True


def part2():
    # For part 2 we want to get the largest connected component. 
    # One could make a node from each computer and then compute the largest conneted 
    # component and get all the names of the nodes and sort them. Could be done with networkx 
    # quite easily.
    
    # But let's do it manually, for good practice let's say.
    data = open("day_23/data_23.txt")
    computer_links = defaultdict(lambda: [])
    pair_set = set()
    unique_computers = set()
    for line in data:

        c1, c2 = line.strip().split("-")
        # Add the pairs to the sets of pairs 
        # We add them in both orders. 
        pair_set.add(frozenset({c1, c2}))
        computer_links[c1].append(c2)
        computer_links[c2].append(c1)

        unique_computers.add(c1)
        unique_computers.add(c2)
    
    # print(computer_links)
    # print(f"####################")
    # Do a second loop over the data
    # lcc = largest connected component
    # cc = connected component
    lcc = set()
    for c1 in unique_computers:
        # if c1 != "ub": continue
        cc = set(computer_links[c1])
        cc.add(c1)
        # print(f"Current computer: {c1} links {cc}")
        for c2 in cc:
            c2_links = set(computer_links[c2])
            c2_links.add(c2)
            # print(f"\nIntersecting {cc} with {c2_links}")
            cc = cc & c2_links
            # print(f"resulting in cc={cc}")
            # Check if the size of cc is larger than lcc
            # We do manually need to check if it is actually a cc
            # Because at this point, we are not sure of it yet.
            if len(cc) > len(lcc) and check_if_cc(cc, pair_set):
                lcc = cc
    # print(f"\n\n\nLargest connected component is:")
    # print(lcc)
    lcc = sorted(list(lcc))
    result = ",".join(lcc)
    # print(lcc)
    # result = ""
    # for c in lcc:
    #     result += c + ","

    print(result)


        

    # data = open("day_23/data_23.txt")
    # for line in data:
    #     c1, c2 = line.strip().split("-")
    #     c1_links = computer_links[c1]
    #     for i in range(len(c1_links) - 1):
    #         for j in range(i + 1, len(c1_links)):
    #             new1, new2 = c1_links[i], c1_links[j]
    #             s = {new1, new2}
    #             if s not in pair_set: continue


s = time()
# part1()
part2()

print(f"{time() - s:.4f}")
