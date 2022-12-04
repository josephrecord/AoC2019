from typing import Tuple


def run(prog: list[int]) -> int:
    # start at beginning of program
    index = 0
    # get opcode
    opcode = prog[index]
    while opcode != 99:
        if opcode == 1:
            # Addition
            operand_1_location = prog[index + 1]
            operand_2_location = prog[index + 2]
            output_location = prog[index + 3]
            opperand1 = prog[operand_1_location]
            opperand2 = prog[operand_2_location]
            output_value = opperand1 + opperand2
            # Overwrite the value at `output_location`
            try:
                prog[output_location] = output_value
            except IndexError:
                # Tried to write past the length of prog
                return -999
            # Move the program counter
            index = index + 4
        elif opcode == 2:
            # Multiplication
            operand_1_location = prog[index + 1]
            operand_2_location = prog[index + 2]
            output_location = prog[index + 3]
            opperand1 = prog[operand_1_location]
            opperand2 = prog[operand_2_location]
            output_value = opperand1 * opperand2
            # Overwrite the value at `output_location`
            try:
                prog[output_location] = output_value
            except IndexError:
                # Tried to write past the length of prog
                return -999
            # Move the program counter
            index = index + 4
        else:
            return -999
        opcode = prog[index]
    return prog[0]


def solve2(prog_initial_state: Tuple[int]) -> int:
    """Find the input noun and verb that cause the
    program to produce the output 19690720. Return 
    100 * noun + verb."""
    # Brute force it...
    for noun in range(100):
        for verb in range(100):
            prog = list(prog_initial_state)
            prog[1] = noun
            prog[2] = verb
            output = run(prog)
            if output == 19690720:
                return 100 * noun + verb



def main() -> None:
    # prog = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    # prog2 = [2, 4, 4, 5, 99, 0]

    with open("input_day2.txt") as f:
        # Make sure initial state is immutable
        prog_initial_state = tuple(int(x) for x in f.readline().split(","))
    
    ans2 = solve2(prog_initial_state)
    print(ans2)


if __name__ == "__main__":
    main()