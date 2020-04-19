import sys


def get_param_modes(operation):
    assert type(operation) == int, "can only get parameter modes for operations"
    s = str(operation)
    l = len(s)
    if l <= 2:
        return 0, 0
    elif l == 3:
        return int(s[0]), 0
    else:
        param_modes = tuple(map(int, reversed(s[:-2])))
        return param_modes


def get_opcode(operation):
    assert type(operation) == int, "opcode needs to be int"
    s = str(operation)
    opcode = int(s[-2:])
    return opcode


def get_num_params(operation):
    assert type(operation) == int, "can only get num params for operations"
    opcode = get_opcode(operation)
    if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
        np = 3
    elif opcode == 3 or opcode == 4 or opcode == 99:
        np = 1
    elif opcode == 5 or opcode == 6:
        np = 2
    else:
        np = "NUM PARAMS ERROR"
    return np


def get_operands(instruct, ip):
    assert type(instruct) == list, "instructions need to be lists of operation+operands"
    assert type(ip) == int, "ip needs to be integer"

    param_modes = get_param_modes(instruct[ip])
    pm0, pm1 = param_modes[0], param_modes[1]
    np = get_num_params(instruct[ip])

    if np == 3:
        if pm0 == 0 and pm1 == 0:
            op1, op2, op3 = instruct[instruct[ip+1]], instruct[instruct[ip+2]], instruct[ip+3]
        elif pm0 == 0 and pm1 == 1:
            op1, op2, op3 = instruct[instruct[ip+1]], instruct[ip+2], instruct[ip+3]
        elif pm0 == 1 and pm1 == 0:
            op1, op2, op3 = instruct[ip+1], instruct[instruct[ip+2]], instruct[ip+3]
        else:
            op1, op2, op3 = instruct[ip+1], instruct[ip+2], instruct[ip+3]
        return [op1, op2, op3]
    elif np == 2:
        if pm0 == 0 and pm1 == 0:
            op1, op2 = instruct[instruct[ip+1]], instruct[instruct[ip+2]]
        elif pm0 == 0 and pm1 == 1:
            op1, op2 = instruct[instruct[ip+1]], instruct[ip+2]
        elif pm0 == 1 and pm1 == 0:
            op1, op2 = instruct[ip+1], instruct[instruct[ip+2]]
        else:
            op1, op2 = instruct[ip+1], instruct[ip+2]
        return [op1, op2]
    elif np == 1:
        if pm0 == 0:
            op1 = instruct[instruct[ip+1]]
        else:
            op1 = instruct[ip+1]
        return [op1]


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
        num_params = get_num_params(instruction)
        print("num params is ", num_params)

        if opcode == 1:
            # addition
            op1, op2, op3 = get_operands(intcode, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            intcode[op3] = op1 + op2
            ip = ip + 4
        elif opcode == 2:
            # multiplication
            op1, op2, op3 = get_operands(intcode, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            intcode[op3] = op1 * op2
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
            op1 = get_operands(intcode, ip)
            print("param1 is ", param1)
            print("OUTPUT: ", op1)
            ip = ip + 2
        elif opcode == 5:
            # jump-if-true: if 1st param is nonzero, set the ip to val from the 2nd param. else, do nothing
            op1, op2 = get_operands(intcode, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            if op1 != 0:
                ip = op2
            else:
                ip = ip + 3
        elif opcode == 6:
            # jump-if-false: if 1st param is 0, set ip to val from the 2nd param. else, do nothing
            op1, op2 = get_operands(intcode, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            if op1 == 0:
                ip = op2
                print("1st param is 0 - new ip is ", ip)
            else:
                ip = ip + 3
        elif opcode == 7:
            # less than: if 1st param < 2nd param, store 1 in the position given by the 3rd param. else, store 0
            op1, op2, op3 = get_operands(intcode, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            if op1 < op2:
                intcode[op3] = 1
            else:
                intcode[op3] = 0
            ip = ip + 4
        elif opcode == 8:
            # equals: if  1st param = 2nd param, store 1 in the position given by the 3rd param. else, store 0
            op1, op2, op3 = get_operands(intcode, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            if op1 == op2:
                intcode[op3] = 1
            else:
                intcode[op3] = 0
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
testprog4 = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
testprog5 = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

prog = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1102, 31, 68, 225, 1001, 13, 87, 224, 1001, 224, -118, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 7, 224, 1, 223, 224, 223, 1, 174, 110, 224, 1001, 224, -46, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 223, 224, 223, 1101, 13, 60, 224, 101, -73, 224, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 224, 223, 223, 1101, 87, 72, 225, 101, 47, 84, 224, 101, -119, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 6, 224, 1, 223, 224, 223, 1101, 76, 31, 225, 1102, 60, 43, 225, 1102, 45, 31, 225, 1102, 63, 9, 225, 2, 170, 122, 224, 1001, 224, -486, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 223, 224, 223, 1102, 29, 17, 224, 101, -493, 224, 224, 4, 224, 102, 8, 223, 223, 101, 1, 224, 224, 1, 223, 224, 223, 1102, 52, 54, 225, 1102, 27, 15, 225, 102, 26, 113, 224, 1001, 224, -1560, 224, 4, 224, 102, 8, 223, 223, 101, 7, 224, 224, 1, 223, 224, 223, 1002, 117, 81, 224, 101, -3645, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1, 223, 224, 223, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 8, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 329, 1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 101, 1, 223, 223, 108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 359, 101, 1, 223, 223, 7, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 374, 101, 1, 223, 223, 1007, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 389, 101, 1, 223, 223, 8, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 404, 1001, 223, 1, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 419, 101, 1, 223, 223, 1108, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 434, 1001, 223, 1, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 449, 101, 1, 223, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 464, 101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 479, 1001, 223, 1, 223, 7, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 494, 1001, 223, 1, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 509, 101, 1, 223, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 524, 101, 1, 223, 223, 1008, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 539, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 554, 101, 1, 223, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 569, 101, 1, 223, 223, 1008, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 584, 101, 1, 223, 223, 8, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 599, 101, 1, 223, 223, 1007, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 614, 101, 1, 223, 223, 1107, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 629, 101, 1, 223, 223, 107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 644, 1001, 223, 1, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 659, 101, 1, 223, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226]


print(run_prog(prog))


