from typing import List, Set, Dict, Tuple
from dataclasses import dataclass, field
from collections import deque
# Then, we also need to store the possible operations
# that need to be done. We need to do a loop, while we're not done
# pick operations that we can do, and remove them from the "to be done"
# operations. This way, or if all the wires have a value, we 
# can stop. Then it is just a matter of looping over 
# all the wires and getting the value in binary and 
# converting it back to a decimal number. 


# We're gonna make the wire a dataclass
# the state of the wire will be stored there, along it's name.

# I made this very readable, and it was definitely overkill.
# But good to brush up on dataclasses again, and on getters
# and setters. Also, I learned that we can sort on the Wire 
# class by adding a sort_index. 

@dataclass
class Wire:
    sort_index: int = field(init=False)
    name: str
    value: bool = None

    def __post_init__(self):
           self.sort_index = self.name

    def set_value(self, value: bool) -> None:
        self.value = value

    def get_value(self):
        return self.value

@dataclass 
class Rule:
    input_wire_1: Wire
    input_wire_2: Wire
    output_wire: Wire
    operator: str
    # inputs: List[Wire, Wire] = [input_wire_1, input_wire_2]
    
    def to_print(self):
        print(f"\n({self.input_wire_1.name}){self.input_wire_1.value} {self.operator} ({self.input_wire_2.name}){self.input_wire_2.value} --> ({self.output_wire.name}){self.output_wire.value}")

    def perform_operation(self) -> None:
        self.v1 = self.input_wire_1.get_value()
        self.v2 = self.input_wire_2.get_value()

        if self.operator == "OR":
            self.or_operator()
        # In the cases of and and xor, neither of the wire values
        # can be none. So if either one of them is, we do not
        # even cover the cases.
        elif self.v1 is None or self.v2 is None:
            return 
        elif self.operator == "AND":
            self.and_operator()
        elif self.operator == "XOR":
            self.xor_operator()
        else:
            assert False

        # self.to_print()

    def or_operator(self) -> None:
        """
            If either one of the operators is True, we can already assign
            the value of the output wire to be True also
        """
        if self.v1 or self.v2: self.output_wire.set_value(True)

        # Check, if both values are not None, then we can properly assign the output value
        if self.v1 is not None and self.v2 is not None:
            self.output_wire.set_value(self.v1 or self.v2)

    def and_operator(self) -> bool:
        self.output_wire.set_value(self.v1 and self.v2)

    def xor_operator(self) -> None:
        """
            Check if both values are the same, but first
            we need a check that they both cannot be None
        """
        self.output_wire.set_value(self.input_wire_1.value ^ self.input_wire_2.value)
        
def all_wires_have_value(all_wires: List[Wire]) -> bool:
    for wire in all_wires:
        if wire.value is None:
            return False
    return True

def get_int_startswith(all_wires: List[Wire], start_with: str) -> int:
    wires = sorted([startswith_wire for startswith_wire in all_wires if startswith_wire.name.startswith(start_with)], key=lambda wire: wire.name)[::-1]
    bin_str = ""
    for wire in wires:
        bin_str += str(int(wire.value))
    return int(bin_str, 2) 

def check_x_y_sum_equals_z(all_wires: List[Wire]) -> bool:
    return get_int_startswith(all_wires, "x") + get_int_startswith(all_wires, "y") == get_int_startswith(all_wires, "z")

def get_wires_and_rules() -> Tuple[Dict[str, Wire], List[Rule]]:
    # First store all the possible wires.
    data = open("day_24/data_24.txt")
    all_rules: List[Rule] = []
    str_to_wire = {}
    initial_values, rules = data.read().split("\n\n")
    initial_values = initial_values.split("\n")
    rules = rules.split("\n")

    # Maybe this loop is redundant.
    for wire in initial_values:
        name, value = wire.split(": ")
        if value == "0":
            value = False
        elif value == "1":
            value = True
        else:
            assert False
        str_to_wire[name] = (Wire(name=name, value=value))
    
    # Now go over all the "rules"
    for rule in rules:
        input_wire1_name, operator, input_wire2_name, _, output_wire_name = rule.strip().split(" ")
        # Check if the wire exists, if so, get it from the dictionry
        # if not, create a new wire without a value, and add it.
        if input_wire1_name not in str_to_wire.keys(): str_to_wire[input_wire1_name] = Wire(name=input_wire1_name)
        input_wire_1 = str_to_wire[input_wire1_name]

        if input_wire2_name not in str_to_wire.keys(): str_to_wire[input_wire2_name] = Wire(name=input_wire2_name)
        input_wire_2 = str_to_wire[input_wire2_name]

        if output_wire_name not in str_to_wire.keys(): str_to_wire[output_wire_name] = Wire(name=output_wire_name)
        output_wire = str_to_wire[output_wire_name]

        # Now add this to the rules
        all_rules.append(Rule(
            input_wire_1=input_wire_1, input_wire_2=input_wire_2, output_wire=output_wire, operator=operator
            )
        )
    return str_to_wire, all_rules


def part1():
    str_to_wire, all_rules = get_wires_and_rules()
    # We are done if all the rules are parsed
    # Or if all the wires have a value, but 
    # this could be equivalent, don't know
    # at this moment in time. Depends on 
    # how the puzzle is made.
    done = False
    while not done:
        rule = all_rules.pop(0)
        rule.perform_operation()
        if rule.output_wire.value is None: all_rules.append(rule)
        if len(all_rules) == 0:
            done = True
    # Just a quick check
    assert all_wires_have_value(str_to_wire.values())
    z_val = get_int_startswith(str_to_wire.values(), "z")
    print(z_val)

"""
    Some helper functions for part 2
"""

def rule_has_inputs_x_y(rule: Rule) -> bool:
    return (rule.input_wire_1.name.startswith("x") and rule.input_wire_2.name.startswith("y")) or (rule.input_wire_1.name.startswith("y") and rule.input_wire_2.name.startswith("x"))

def part2():
    """
        Implementation from: https://www.bytesizego.com/blog/aoc-day24-golang
    """

    # If the ouptut is a "z" wire, then the operation has to be XOR, except for the last bit.
    # The last "z" bit (by inspection) is z45
    # First store all the possible wires.
    _, all_rules = get_wires_and_rules()
    faulty_rules = []
    for rule in all_rules:
        to_swap = rule.output_wire.name
        # Rule 1
        # If the output is z, then the operator needs to be XOR except for the last bit.
        if rule.output_wire.name.startswith("z") and rule.operator != "XOR" and rule.output_wire.name != "z45":
            faulty_rules.append(to_swap)
            continue

        # Rule 2
        # If the output is not z, and the inputs are not x and y, then the operator needs to be AND or OR, but not XOR
        if not rule.output_wire.name.startswith("z") and not rule_has_inputs_x_y(rule) and rule.operator == "XOR":
            faulty_rules.append(to_swap)
            continue

        # Rule 3
        # If there is an XOR gate with inputs x and y 
        if rule.operator == "XOR" and rule_has_inputs_x_y(rule) and rule.input_wire_1.name != "x00" and rule.input_wire_2.name != "x00":
            # Then there must be another gate (XOR) so that any of the inputs is the output of the loopvariable "rule"
            found = False
            # Check for all the rules, if the output wire is in any of the "XOR" gates. If it is, the original gate (loop "rule") is faulty.
            for new_rule in all_rules:
                if new_rule.operator == "XOR" and (new_rule.input_wire_1.name == rule.output_wire.name or new_rule.input_wire_2.name == rule.output_wire.name):
                    found = True
                    break
            if not found:
                faulty_rules.append(to_swap)
                continue

        # Rule 4
        if rule.operator == "AND" and rule_has_inputs_x_y(rule) and rule.input_wire_1.name != "x00" and rule.input_wire_2.name != "x00":
            # Then there must be another gate (XOR) so that any of the inputs is the output of the loopvariable "rule"
            found = False
            for new_rule in all_rules:
                if new_rule.operator == "OR" and new_rule.input_wire_1.name == rule.output_wire.name or new_rule.input_wire_2.name == rule.output_wire.name:
                    found = True
                    break
            if not found:
                faulty_rules.append(to_swap)
                continue


    print(len(faulty_rules))
    faulty_rules = sorted(faulty_rules)
    print(",".join(faulty_rules))

part2()


# The swapping is very tedious...
