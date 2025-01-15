import re

from typing import List

data = open("day_3/data_3.txt")
data = data.read()
# Template with number
template = r"mul\(\d+,\d+\)"
templates = [
    r"mul\(\d+,\d+\)",        # Template for numbers
    r"do\(\)",      # Template with single quotes around first number
    r"don't\(\)"     # Template with single quotes around both numbers
]


combined_template = "|".join(templates)
print(combined_template)

# Find all matches using re.finditer
matches = re.findall(combined_template, data)
print(matches)
# Collect and display all matches
# results = [match.group() for match in matches]
# print("Matches found:", results)

def multiply(str_mul) -> int:
    a, b = str_mul.split("mul(")[-1][:-1].split(",")
    return int(a) * int(b)

def change_do(do_str: str, dont: bool) -> bool:
    if "mul" in do_str:
        return dont
    elif "t" in do_str:
        return True
    else:
        return False
    
dont = False
total = 0
for match in matches:
    dont = change_do(match, dont)
    if dont or "mul" not in match:
        continue
    total += multiply(match)
    print("multiply found:", match)
    

print(total)
