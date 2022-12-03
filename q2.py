
prog = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
prog2 = [2,4,4,5,99,0]

with open("input_day2.txt") as f:
    input = [int(x) for x in f.readline().split(",")]

# before running the program, replace position 1 with the value 12
# and replace position 2 with the value 2. What value is left at 
# position 0 after the program halts?
input[1] = 12
input[2] = 2

def run(prog):
    # start at beginning of program
    index = 0
    # get opcode
    opcode = prog[index]
    while opcode != 99:
        if opcode == 1:
            # Addition
            print(f"Addition: {prog[index:index+4]}")
            operand_1_location = prog[index + 1]
            operand_2_location = prog[index + 2]
            output_location = prog[index + 3]
            opperand1 = prog[operand_1_location]
            opperand2 = prog[operand_2_location]
            output_value = opperand1 + opperand2
            print(output_value)
            # Overwrite the value at `output_location`
            prog[output_location] = output_value
            # Move the program counter
            index = index + 4
        elif opcode == 2:
            # Multiplication
            print(f"Multiplication: {prog[index:index+4]}")
            operand_1_location = prog[index + 1]
            operand_2_location = prog[index + 2]
            output_location = prog[index + 3]
            opperand1 = prog[operand_1_location]
            opperand2 = prog[operand_2_location]
            output_value = opperand1 * opperand2
            print(output_value)
            # Overwrite the value at `output_location`
            prog[output_location] = output_value
            # Move the program counter
            index = index + 4
        opcode = prog[index]
    return prog

run(input)
        