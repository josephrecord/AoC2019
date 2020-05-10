import sys

def mem_write(tup: tuple, i: int, v: int) -> tuple:
    # write a value at an index >= length(tuple)
    # fills with None until desired index
    # e.g. a = (1, 2, 5, 4)
    # expand_write(a, 6, 9) ==> (1, 2, 5, 4, None, None, 9)
    assert type(tup) == tuple, "input must be a tuple"
    assert type(i) == int, "i must be an int"
    assert i >= 0, "index must be positive"
    assert i <= 34463338, "index out of range"
    mem_vals = list(tup)
    mem_len = len(mem_vals)
    if i < mem_len:
        mem_vals[i] = v
    else:
        current_index = mem_len
        while current_index != i:
            mem_vals.append(0)
            current_index += 1
        mem_vals.append(v)
    return tuple(mem_vals)


def mem_read(tup: tuple, i: int) -> int:
    assert type(tup) == tuple, "input must be a tuple"
    assert type(i) == int, "i must be an int"
    assert i >= 0, "index must be positive"
    mem_len = len(tup)
    mem_vals = list(tup)
    if i > mem_len:
        return 0
    return mem_vals[i]


def get_opcode(operation):
    assert type(operation) == int, "opcode needs to be int"
    s = str(operation)
    opcode = int(s[-2:])
    return opcode


def get_num_params(operation):
    assert type(operation) == int, "can only get num params for operations"
    opcode = get_opcode(operation)
    if opcode == 99:
        np = 0
    elif opcode == 3 or opcode == 4 or opcode ==9:
        np = 1
    elif opcode == 5 or opcode == 6:
        np = 2
    elif opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:
        np = 3
    else:
        print("NUM PARAMS ERROR")
        sys.exit()
    return np


def get_param_modes(operation):
    assert type(operation) == int, "can only get parameter modes for operations"
    np = get_num_params(operation)
    str_op = str(operation)
    length = len(str_op)
    if np == 1:
        if length <= 2:
            return 0
        else:
            return int(str_op[-3])
    elif np == 2:
        if length <= 2:
            return 0, 0
        elif length == 3:
            return int(str_op[-3]), 0
        else:
            return int(str_op[-3]), int(str_op[-4])
    else:
        if length <= 2:
            return 0, 0, 0
        elif length == 3:
            return int(str_op[-3]), 0, 0
        elif length == 4:
            return int(str_op[-3]), int(str_op[-4]), 0
        elif length >= 5:
            return int(str_op[-3]), int(str_op[-4]), int(str_op[-5])
        else:
            print("param modes error")
            return "param modes error"


def get_operands(instruct, ip, rbo):
    # assert type(instruct) == list, "instructions need to be lists of operation+operands"
    assert type(ip) == int, "ip needs to be integer"
    operation = instruct[ip]
    np = get_num_params(operation)
    parameters = get_param_modes(operation)
    if np == 3:
        param1, param2, param3 = parameters[0], parameters[1], parameters[2]
        if param1 == 0 and param2 == 0:
            op1, op2 = instruct[instruct[ip+1]], instruct[instruct[ip+2]]
        elif param1 == 0 and param2 == 1:
            op1, op2 = instruct[instruct[ip+1]], instruct[ip+2]
        elif param1 == 0 and param2 == 2:
            op1, op2 = instruct[instruct[ip + 1]], instruct[instruct[rbo]]
        elif param1 == 1 and param2 == 0:
            op1, op2 = instruct[ip+1], instruct[instruct[ip+2]]
        elif param1 == 1 and param2 == 1:
            op1, op2 = instruct[ip+1], instruct[ip+2]
        elif param1 == 1 and param2 == 2:
            op1, op2 = instruct[ip+1], instruct[instruct[rbo]]
        elif param1 == 2 and param2 == 0:
            op1, op2 = instruct[instruct[rbo]], instruct[instruct[ip+2]]
        elif param1 == 2 and param2 == 1:
            op1, op2 = instruct[instruct[rbo]], instruct[ip+2]
        elif param1 == 2 and param2 == 2:
            op1, op2 = instruct[instruct[rbo]], instruct[instruct[rbo]]
        return op1, op2
    elif np == 2:
        param1, param2 = parameters[0], parameters[1]
        if param1 == 0 and param2 == 0:
            op1, op2 = instruct[instruct[ip+1]], instruct[instruct[ip+2]]
        elif param1 == 0 and param2 == 1:
            op1, op2 = instruct[instruct[ip+1]], instruct[ip+2]
        elif param1 == 0 and param2 == 2:
            op1, op2 = instruct[instruct[ip + 1]], instruct[instruct[rbo]]
        elif param1 == 1 and param2 == 0:
            op1, op2 = instruct[ip+1], instruct[instruct[ip+2]]
        elif param1 == 1 and param2 == 1:
            op1, op2 = instruct[ip+1], instruct[ip+2]
        elif param1 == 1 and param2 == 2:
            op1, op2 = instruct[ip+1], instruct[instruct[rbo]]
        elif param1 == 2 and param2 == 0:
            op1, op2 = instruct[instruct[rbo]], instruct[instruct[ip+2]]
        elif param1 == 2 and param2 == 1:
            op1, op2 = instruct[instruct[rbo]], instruct[ip+2]
        elif param1 == 2 and param2 == 2:
            op1, op2 = instruct[instruct[rbo]], instruct[instruct[rbo]]
        return op1, op2
    elif np == 1:
        param1 = parameters[0]
        if param1 == 0:
            op1 = instruct[instruct[ip+1]]
        elif param1 == 1:
            op1 = instruct[ip+1]
        elif param == 2:
            rbo += instruct[ip+1]
            op1 = rbo
        else:
            print("im here")
        return op1


def compute(program):
    assert type(program) is tuple, "program must be a tuple"
    program = list(program)
    ip = 0
    rbo = 0

    while True:
        instruction = program[ip]
        opcode = get_opcode(instruction)

        if opcode == 1:
            op1, op2, op3 = get_operands(program, ip)
            result = op1 + op2
            mem_write(program, i, result)
            ip = ip + 4
        elif opcode == 2:
            op1, op2, op3 = get_operands(program, ip)
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
        elif opcode == 9:
            # adjusts the relative base by the value of its only parameter
            rbo += program[ip+1]
        elif opcode == 99:
            halt = True
            prog_out = last_out
            return tuple(program), ip, prog_out, halt
        else:
            print("ERROR - OPCODE ", opcode, " NOT VALID")
            sys.exit()


p = (109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99)