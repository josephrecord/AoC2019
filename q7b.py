import itertools
import sys
global halt
global lastout
lastout = 0

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


def amp(program, ip, inputs, last_out):
    # phase setting is in1, output of prev amplifier is in2
    program = list(program)
    input_index = 0

    while True:
        # print("program is ", program)
        instruction = program[ip]
        # print("instruction is ", instruction)
        opcode = get_opcode(instruction)
        # print("opcode is ", opcode)
        param_modes = get_param_modes(instruction)
        # print("param modes are ", param_modes)
        num_params = get_num_params(instruction)
        # print("num params is ", num_params)
        halt = False

        if opcode == 1:
            # addition
            op1, op2, op3 = get_operands(program, ip)
            # print("operand 1 is ", op1)
            # print("operand 2 is ", op2)
            # print("operand 3 is ", op3)
            program[op3] = op1 + op2
            ip = ip + 4
        elif opcode == 2:
            # multiplication
            op1, op2, op3 = get_operands(program, ip)
            # print("operand 1 is ", op1)
            # print("operand 2 is ", op2)
            # print("operand 3 is ", op3)
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
            lastout = prog_out
            # print("param1 is ", param1)
            # print("OUTPUT: ", op1)
            ip = ip + 2
            return tuple(program), ip, prog_out, halt
        elif opcode == 5:
            # jump-if-true: if 1st param is nonzero, set the ip to val from the 2nd param. else, do nothing
            op1, op2 = get_operands(program, ip)
            # print("operand 1 is ", op1)
            # print("operand 2 is ", op2)
            # print("operand 3 is ", op3)
            if op1 != 0:
                ip = op2
            else:
                ip = ip + 3
        elif opcode == 6:
            # jump-if-false: if 1st param is 0, set ip to val from the 2nd param. else, do nothing
            op1, op2 = get_operands(program, ip)
            # print("operand 1 is ", op1)
            # print("operand 2 is ", op2)
            # print("operand 3 is ", op3)
            if op1 == 0:
                ip = op2
                # print("1st param is 0 - new ip is ", ip)
            else:
                ip = ip + 3
        elif opcode == 7:
            # less than: if 1st param < 2nd param, store 1 in the position given by the 3rd param. else, store 0
            op1, op2, op3 = get_operands(program, ip)
            # print("operand 1 is ", op1)
            # print("operand 2 is ", op2)
            # print("operand 3 is ", op3)
            if op1 < op2:
                program[op3] = 1
            else:
                program[op3] = 0
            ip = ip + 4
        elif opcode == 8:
            # equals: if  1st param = 2nd param, store 1 in the position given by the 3rd param. else, store 0
            op1, op2, op3 = get_operands(program, ip)
            # print("operand 1 is ", op1)
            # print("operand 2 is ", op2)
            # print("operand 3 is ", op3)
            if op1 == op2:
                program[op3] = 1
            else:
                program[op3] = 0
            ip = ip + 4
        elif opcode == 99:
            halt = True
            prog_out = last_out
            return tuple(program), ip, prog_out, halt
        else:
            # print("ERROR - OPCODE ", opcode, " NOT VALID")
            sys.exit()


ans = []
phase_seqs = list(itertools.permutations("56789"))


for phase in phase_seqs:
    phase1 = int(phase[0])
    phase2 = int(phase[1])
    phase3 = int(phase[2])
    phase4 = int(phase[3])
    phase5 = int(phase[4])

    prog = [3,8,1001,8,10,8,105,1,0,0,21,38,47,64,85,106,187,268,349,430,99999,3,9,1002,9,4,9,1001,9,4,9,1002,9,4,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,1001,9,3,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,101,3,9,9,102,5,9,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,1002,9,3,9,101,2,9,9,102,4,9,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]


    ip1 = 0
    ip2 = 0
    ip3 = 0
    ip4 = 0
    ip5 = 0

    halt = False
    count = 0


    prog1, ip1, out1, halt = amp(prog, ip1, [phase1, 0], 0)

    prog2, ip2, out2, halt = amp(prog, ip2, [phase2, out1], 0)

    prog3, ip3, out3, halt = amp(prog, ip3, [phase3, out2], 0)

    prog4, ip4, out4, halt = amp(prog, ip4, [phase4, out3], 0)

    prog5, ip5, out5, halt = amp(prog, ip5, [phase5, out4], 0)

    result = out5

    while halt == False:
        prog1, ip1, out1, halt = amp(prog1, ip1, [out5], out1)
        prog2, ip2, out2, halt = amp(prog2, ip2, [out1], out2)
        prog3, ip3, out3, halt = amp(prog3, ip3, [out2], out3)
        prog4, ip4, out4, halt = amp(prog4, ip4, [out3], out4)
        prog5, ip5, out5, halt = amp(prog5, ip5, [out4], out5)
        result = out5
        count += 1

    ans.append(out5)

print(max(ans))



