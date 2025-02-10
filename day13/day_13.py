from typing import List, Tuple


def print_eq(equation):
    x1, x2, tx, y1, y2, ty = equation
    print(f"a{x1} + b{x2} = {tx}\na{y1} + b{y2} = {ty}\n")

def parse_data(part2: bool = False) -> List[Tuple[int, int, int, int, int, int]]:
    data = open("day_13/data_13.txt")
    text = data.read().split("\n\n")
    equations = []

    for eq in text:
        eq1, eq2, eq3 = eq.split("\n")
        x1, y1 = int(eq1.split(" ")[-2].split("+")[-1][:-1]), int(eq1.split(" ")[-1].split("+")[-1])
        x2, y2 = int(eq2.split(" ")[-2].split("+")[-1][:-1]), int(eq2.split(" ")[-1].split("+")[-1])
        tx, ty = int(eq3.split(" ")[-2].split("=")[-1][:-1]), int(eq3.split(" ")[-1].split("=")[-1])

        if part2:
            tx += 10 **13
            ty += 10 **13
        equations.append((x1, x2, tx, y1, y2, ty))
    return equations

def calculate_options(equation: str) -> List[Tuple[int, int]]:
    x1, x2, tx, y1, y2, ty = equation
    for a in range(0, 101):
        for b in range(0, 101):
            if a * x1 + b * x2 == tx and a * y1 + b * y2 == ty:
                return (a,b)
    return []
    
def get_cost_from_solution(solution: Tuple[int, int]) -> int:
    a, b = solution
    return 3 * a + b

# print(equations)
def part1():
    equations = parse_data()
    num_no_solutions = 0
    total_num_tokens = 0
    for equation in equations:
        # print(f"\nParsing equation: {equation}")
        solution = calculate_options(equation)
        if len(solution) == 0:
            # print(f"No solution for:\n")
            num_no_solutions += 1
            # print_eq(equation)
            continue
        total_num_tokens += get_cost_from_solution(solution)
        
            
        

    print(f"Total number of tokens: {total_num_tokens}")
    print(f"In total {num_no_solutions}/{len(equations)} equations had no solution")


# part1()

# Of course the naive way doesn't work for part 2.
# after doing some calculations on paper, we can immediately compute
# the solutions. We only need to check that both entries are nonnegative

def compute_instantly(equation) -> int:
    x1, x2, tx, y1, y2, ty = equation
    a = (tx * y2 - ty * x2) / (x1 * y2 - y1 * x2)
    b = (tx * y1 - ty * x1) / (x2 * y1 - y2 * x1)
    return (a, b)

def part2():
    equations = parse_data(part2=True)
    total = 0
    for equation in equations:
        a, b = compute_instantly(equation)  
        if a < 0 or b < 0:
            # solution not possible
            continue
        if not a.is_integer() or not b.is_integer():
            continue
        # print_eq(equation)
        # print((a, b))
        total += int(get_cost_from_solution((a, b)))
    print(f"Second method:")
    print(total)


part2()
