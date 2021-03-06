import sys
import itertools


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
    i = 0
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


def amplifier(program, inputs):
    # phase setting is in1, output of prev amplifier is in2
    assert type(program) == list, "program must be a list"
    ip = 0
    input_index = 0

    while True:
        print("program is ", program)
        instruction = program[ip]
        print("instruction is ", instruction)
        opcode = get_opcode(instruction)
        print("opcode is ", opcode)
        param_modes = get_param_modes(instruction)
        print("param modes are ", param_modes)
        num_params = get_num_params(instruction)
        print("num params is ", num_params)

        if opcode == 1:
            # addition
            op1, op2, op3 = get_operands(program, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            program[op3] = op1 + op2
            ip = ip + 4
        elif opcode == 2:
            # multiplication
            op1, op2, op3 = get_operands(program, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            program[op3] = op1 * op2
            ip = ip + 4
        elif opcode == 3:
            # takes a single integer as input and saves it to the position given by its only parameter
            param1 = program[ip + 1]
            # user_input = int(input("Enter a value: "))
            program[param1] = inputs[input_index]
            input_index += 1
            ip = ip + 2
        elif opcode == 4:
            # outputs the value of its only parameter
            param1 = program[ip + 1]
            op1 = get_operands(program, ip)
            prog_out = int(op1[0])
            # print("param1 is ", param1)
            print("OUTPUT: ", op1)
            ip = ip + 2
        elif opcode == 5:
            # jump-if-true: if 1st param is nonzero, set the ip to val from the 2nd param. else, do nothing
            op1, op2 = get_operands(program, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            if op1 != 0:
                ip = op2
            else:
                ip = ip + 3
        elif opcode == 6:
            # jump-if-false: if 1st param is 0, set ip to val from the 2nd param. else, do nothing
            op1, op2 = get_operands(program, ip)
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
            op1, op2, op3 = get_operands(program, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            if op1 < op2:
                program[op3] = 1
            else:
                program[op3] = 0
            ip = ip + 4
        elif opcode == 8:
            # equals: if  1st param = 2nd param, store 1 in the position given by the 3rd param. else, store 0
            op1, op2, op3 = get_operands(program, ip)
            print("operand 1 is ", op1)
            print("operand 2 is ", op2)
            print("operand 3 is ", op3)
            if op1 == op2:
                program[op3] = 1
            else:
                program[op3] = 0
            ip = ip + 4
        elif opcode == 99:
            print("END OF GOOD PROGRAM")
            return prog_out
        else:
            print("ERROR - OPCODE ", opcode, " NOT VALID")
            sys.exit()



ans = []
prog = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
prog2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
p = [3,8,1001,8,10,8,105,1,0,0,21,38,47,64,85,106,187,268,349,430,99999,3,9,1002,9,4,9,1001,9,4,9,1002,9,4,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,1001,9,3,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,101,3,9,9,102,5,9,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,1002,9,3,9,101,2,9,9,102,4,9,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]
phase_sequence = [4, 3, 2, 1, 0]

phase_seqs = list(itertools.permutations("01234"))

for phase in phase_seqs:
    in1 = int(phase[0])
    in2 = int(phase[1])
    in3 = int(phase[2])
    in4 = int(phase[3])
    in5 = int(phase[4])

    print(in1, in2, in3, in4, in5)


    out1 = amplifier(p, [in1, 0])
    print("amp 1 output: ", out1)
    out2 = amplifier(p, [in2, out1])
    out3 = amplifier(p, [in3, out2])
    out4 = amplifier(p, [in4, out3])
    out5 = amplifier(p, [in5, out4])

    ans.append(out5)

print(max(ans))










