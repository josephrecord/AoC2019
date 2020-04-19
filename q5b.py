import sys


def get_param_modes(instruct):
    s = str(instruct)
    l = len(s)
    if l <= 2:
        return 0, 0
    elif l == 3:
        return int(s[0]), 0
    else:
        param_modes = tuple(map(int, reversed(s[:-2])))
        return param_modes


def get_opcode(instruct):
    s = str(instruct)
    opcode = int(s[-2:])
    return opcode


def run_prog(intcode):
    ip = 0

    while True:
        print("intcode is ", intcode)
        instruction = intcode[ip]
        print("instruction is ", instruction)
        opcode = get_opcode(instruction)
        print("opcode is ", opcode)
        param_modes = get_param_modes(instruction)
        print("param modes are ", param_modes)

        if opcode == 1:
            # addition
            param1, param2, param3 = intcode[ip + 1], intcode[ip + 2], intcode[ip + 3]
            print("addition")
            print(param1, intcode[param1])
            print(param2, intcode[param2])
            print(param3, intcode[param3])
            if param_modes[0] == 0 and param_modes[1] == 0:
                intcode[param3] = intcode[param1] + intcode[param2]
                print("intcode param3 ", param3, "is ", intcode[param3])
            elif param_modes[0] == 1 and param_modes[1] == 1:
                intcode[param3] = param1 + param2
            elif param_modes[0] == 1 and param_modes[1] == 0:
                intcode[param3] = param1 + intcode[param2]
            elif param_modes[0] == 0 and param_modes[1] == 1:
                intcode[param3] = intcode[param1] + param2
            else: print("oops")
            ip = ip + 4
        elif opcode == 2:
            # multiplication
            param1, param2, param3 = intcode[ip + 1], intcode[ip + 2], intcode[ip + 3]
            print("mult")
            if param_modes[0] == 0 and param_modes[1] == 0:
                intcode[param3] = intcode[param1] * intcode[param2]
            elif param_modes[0] == 1 and param_modes[1] == 1:
                intcode[param3] = param1 * param2
            elif param_modes[0] == 1 and param_modes[1] == 0:
                intcode[param3] = param1 * intcode[param2]
            elif param_modes[0] == 0 and param_modes[1] == 1:
                intcode[param3] = intcode[param1] * param2
            else: print("oopsies")
            ip = ip + 4
        elif opcode == 3:
            # takes a single integer as input and saves it to the position given by its only parameter
            param1 = intcode[ip + 1]
            user_input = int(input("Enter a value: "))
            intcode[param1] = user_input
            ip = ip + 2
        elif opcode == 4:
            # outputs the value of its only parameter
            param1 = intcode[ip + 1]
            print("OUTPUT: ", intcode[param1])
            ip = ip + 2
        elif opcode == 5:
            # jump-if-true: if 1st param is nonzero, set the ip to val from the 2nd param. else, do nothing
            param1, param2 = intcode[ip + 1], intcode[ip + 2]
            if intcode[param1] != 0:
                ip = param2
            else:
                ip = ip + 3
        elif opcode == 6:
            # jump-if-false: if 1st param is 0, set ip to val from the 2nd param. else, do nothing
            param1, param2 = intcode[ip + 1], intcode[ip + 2]
            print(param1)
            print(param2)
            if intcode[param1] == 0:
                ip = intcode[param2]
                print("1st param is 0 - new ip is ", ip)
            else:
                ip = ip + 3
                print("new ip +3 is ", ip)
        elif opcode == 7:
            # less than: if 1st param < 2nd param, store 1 in the position given by the 3rd param. else, store 0
            param1, param2, param3 = intcode[ip + 1], intcode[ip + 2], intcode[ip + 3]
            if intcode[param1] < intcode[param2]:
                intcode[param3] = 1
            else:
                intcode[param3] = 0
            ip = ip + 4
        elif opcode == 8:
            # equals: if  1st param = 2nd param, store 1 in the position given by the 3rd param. else, store 0
            param1, param2, param3 = intcode[ip + 1], intcode[ip + 2], intcode[ip + 3]
            if intcode[param1] == intcode[param2]:
                intcode[param3] = 1
            else:
                intcode[param3] = 0
            ip = ip + 4
        elif opcode == 99:
            print("END OF GOOD PROGRAM")
            return intcode
        else:
            print("ERROR - OPCODE ", opcode, " NOT VALID")
            sys.exit()


testprog1 = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8] # Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
testprog2 = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8] # Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
testprog3 = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9] # jump test that takes an input, then output 0 if the input was zero or 1 if the input was non-zero

print(run_prog(testprog3))


