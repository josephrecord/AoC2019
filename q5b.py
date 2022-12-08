from typing import Tuple


def interpret_command(ABCDE: int) -> Tuple[int, list[int]]:
    """
    ABCDE   <-- Let's call this a command
     1002
    DE - two-digit opcode,      02 == opcode 2
    C - mode of 1st parameter,  0 == position mode
    B - mode of 2nd parameter,  1 == immediate mode
    A - mode of 3rd parameter,  0 == position mode, omitted due to being a leading zero
    """
    opcode = int(str(ABCDE)[-2:])   # opcode is last two digits
    param_modes = []
    for digit in str(ABCDE)[:-2]:
        param_modes.append(int(digit))
    return opcode, param_modes


def pop_param_mode(param_mode_list: list[int]) -> int:
    try:
        return param_mode_list.pop()
    except IndexError:
        return 0



def run(prog: list[int]) -> int:
    # start at beginning of program
    instruction_pointer = 0
    # get opcode
    opcode, param_modes = interpret_command(prog[instruction_pointer])
    while opcode != 99:
        # print(f"Instruction pointer: {instruction_pointer}")
        if opcode == 1:
            # Addition
            param1_mode = pop_param_mode(param_modes)
            if param1_mode == 0:   # Position mode (standard)
                param1 = prog[instruction_pointer + 1]
                opperand1 = prog[param1]
            elif param1_mode == 1: # Immediate mode (new)
                param1 = prog[instruction_pointer + 1]
                opperand1 = param1
            else:
                raise ValueError(f"Improper param mode in Addition {prog[instruction_pointer:instruction_pointer+4]}")
            
            param2_mode = pop_param_mode(param_modes)
            if param2_mode == 0:   # Position mode (standard)
                param2 = prog[instruction_pointer + 2]
                opperand2 = prog[param2]
            elif param2_mode == 1: # Immediate mode (new)
                param2 = prog[instruction_pointer + 2]
                opperand2 = param2
            else:
                raise ValueError(f"Improper param mode in Addition {prog[instruction_pointer:instruction_pointer+4]}")
            
            output_value = opperand1 + opperand2
            param3 = prog[instruction_pointer + 3]  # Third param in addition is the output address
            # Parameters that an instruction writes to will never be in immediate mode.
            # Overwrite the value at `output_location`
            try:
                prog[param3] = output_value
            except IndexError:
                # Tried to write past the length of prog
                return -999
            # Move the program counter
            instruction_pointer += 4
        
        elif opcode == 2:
            # Multiplication
            param1_mode = pop_param_mode(param_modes)
            if param1_mode == 0:   # Position mode (standard)
                param1 = prog[instruction_pointer + 1]
                opperand1 = prog[param1]
            elif param1_mode == 1: # Immediate mode (new)
                param1 = prog[instruction_pointer + 1]
                opperand1 = param1
            else:
                raise ValueError(f"Invalid param mode in mult {prog[instruction_pointer:instruction_pointer+4]}")
            
            param2_mode = pop_param_mode(param_modes)
            if param2_mode == 0:   # Position mode (standard)
                param2 = prog[instruction_pointer + 2]
                opperand2 = prog[param2]  # In position mode, the param is interpreted as an address
            elif param2_mode == 1: # Immediate mode (new)
                param2 = prog[instruction_pointer + 2]
                opperand2 = param2
            else:
                raise ValueError(f"Invalid param mode in mult {prog[instruction_pointer:instruction_pointer+4]}")
            
            output_value = opperand1 * opperand2
            param3 = prog[instruction_pointer + 3]  # Third param in addition is the output address
            # Parameters that an instruction writes to will never be in immediate mode.
            # Overwrite the value at `output_location`
            try:
                prog[param3] = output_value
            except IndexError:
                # Tried to write past the length of prog
                return -999
            # Move the program counter
            instruction_pointer += 4
        
        elif opcode == 3:
            # Save user input to program
            # Opcode 3 takes a single integer as input and saves
            # it to the position given by its only parameter. 
            # For example, the instruction 3,50 would take an 
            # input value and store it at address 50.
            user_input = int(input("Enter a number: "))
            # Overwrite the value at the location given by the parameter.
            save_location = prog[instruction_pointer + 1]
            try:
                prog[save_location] = user_input
            except IndexError:
                # Tried to write past the length of prog
                return -999
            instruction_pointer += 2
        
        elif opcode == 4:
            # Opcode 4 outputs the value of its only parameter.
            # For example, the instruction 4,50 would output
            # the value at address 50.
            param1 = prog[instruction_pointer + 1]
            output_val = prog[param1]
            print(f"Output: {output_val}")
            instruction_pointer += 2
        
        elif opcode == 5:
            # jump-if-true: if the first parameter is non-zero,
            # it sets the instruction pointer to the value from
            # the second parameter. Otherwise, it does nothing.
            param1 = prog[instruction_pointer + 1]
            if param1 != 0: # True, so jump
                param1_mode = pop_param_mode(param_modes)
                if param1_mode == 0:
                    pass
        else:
            return -999
        # Get the next opcode and parameter modes at the new instruction pointer
        opcode, param_modes = interpret_command(prog[instruction_pointer])
    return prog


def solve2(prog: Tuple[int, ...]) -> int:
    prog = list(prog)
    run(prog)


def main() -> None:

    with open("input5.txt") as f:
        # Make sure initial state is immutable
        prog_initial_state = tuple(int(x) for x in f.readline().split(","))
    
    t1 = (3,9,8,9,10,9,4,9,99,-1,8) # Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
    tx = (3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9)

    ans2 = solve2(t1)
    print(ans2)


if __name__ == "__main__":
    main()