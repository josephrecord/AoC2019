import sys


def mem_write(program, address: int, val: int) -> list:
    # write a value at an index >= length(tuple)
    # fills with None until desired index
    # e.g. a = (1, 2, 5, 4)
    # expand_write(a, 6, 9) ==> (1, 2, 5, 4, 0, 0, 9)
    assert type(address) == int, "i must be an int"
    assert address >= 0, "index must be positive"
    assert address <= 34463338, "index out of range"
    mem_len = len(program)
    if address < mem_len:
        program[address] = val
    else:
        current_index = mem_len
        while current_index != address:
            program.append(0)
            current_index += 1
        program.append(val)
    return program


def mem_read(program, address: int) -> int:
    assert type(address) == int, "i must be an int"
    assert address >= 0, "index must be positive"
    mem_len = len(program)
    if address >= mem_len:
        return 0
    return program[address]


def get_opcode(operation):
    assert type(operation) == int, "opcode needs to be int"
    s = str(operation)
    opcode = int(s[-2:])
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
    return opcode, np


def get_param_modes(operation):
    assert type(operation) == int, "can only get parameter modes for operations"
    opcode, np = get_opcode(operation)
    str_op = str(operation)
    length = len(str_op)
    if np == 1:
        if length <= 2:
            return [0]
        else:
            return [int(str_op[-3])]
    elif np == 2:
        if length <= 2:
            return [0, 0]
        elif length == 3:
            return [int(str_op[-3]), 0]
        else:
            return [int(str_op[-3]), int(str_op[-4])]
    else:
        if length <= 2:
            return [0, 0, 0]
        elif length == 3:
            return [int(str_op[-3]), 0, 0]
        elif length == 4:
            return [int(str_op[-3]), int(str_op[-4]), 0]
        elif length >= 5:
            return [int(str_op[-3]), int(str_op[-4]), int(str_op[-5])]
        else:
            print("param modes error")
            return "param modes error"


def get_params(program, ip):
    operation = program[ip]
    op, np = get_opcode(operation)
    param_modes = get_param_modes(operation)
    params = []
    for p in range(np):
        params.append(program[ip + p+1])
    return list(zip(params, param_modes))


def compute(program):
    # assert type(program) is tuple, "program must be a tuple"

    ip = 0
    rb = 0

    while True:
        # print(program)
        instruction = program[ip]
        opcode, np = get_opcode(instruction)

        if opcode == 1:
            operands = get_operands(program, ip, rb)
            result = operands[0] + operands[1]
            program = mem_write(program, program[ip + 3], result)
            ip = ip + 4
        elif opcode == 2:
            operands = get_operands(program, ip, rb)
            result = operands[0] * operands[1]
            program = mem_write(program, program[ip + 3], result)
            ip = ip + 4
        elif opcode == 3:
            # takes a single integer as input and saves it to the position given by its only parameter
            operand = get_operands(program, ip, rb)
            user_input = int(input("Enter a value: "))
            program = mem_write(program, operand[0], user_input)
            ip = ip + 2
        elif opcode == 4:
            # outputs the value of its only parameter
            operand = get_operands(program, ip, rb)
            op1 = operand[0]
            output = mem_read(program, op1)
            print("OUTPUT: ", output)
            if output == [99]:
                sys.exit()
            ip = ip + 2
        elif opcode == 5:
            # jump-if-true: if 1st param is nonzero, set the ip to val from the 2nd param. else, do nothing
            operands = get_operands(program, ip, rb)
            op1, op2 = operands[0], operands[1]
            if op1 != 0:
                ip = op2
            else:
                ip = ip + 3
        elif opcode == 6:
            # jump-if-false: if 1st param is 0, set ip to val from the 2nd param. else, do nothing
            operands = get_operands(program, ip, rb)
            op1, op2 = operands[0], operands[1]
            if op1 == 0:
                ip = op2
            else:
                ip = ip + 3
        elif opcode == 7:
            # less than: if 1st param < 2nd param, store 1 in the position given by the 3rd param. else, store 0
            operands = get_operands(program, ip, rb)
            op1, op2, op3 = operands[0], operands[1], operands[2]
            if op1 < op2:
                program = mem_write(program, program[ip + 3], 1)
            else:
                program = mem_write(program, program[ip + 3], 0)
            ip = ip + 4
        elif opcode == 8:
            # equals: if  1st param = 2nd param, store 1 in the position given by the 3rd param. else, store 0
            operands = get_operands(program, ip, rb)
            op1, op2, op3 = operands[0], operands[1], operands[2]
            if op1 == op2:
                program = mem_write(program, program[ip + 3], 1)
            else:
                program = mem_write(program, program[ip + 3], 0)
            ip = ip + 4
        elif opcode == 9:
            # adjusts the relative base by the value of its only parameter
            params = get_params(program, ip)
            for i in range(len(params)):
                param, param_mode = params[i]
                if param_mode == 1:
                    rb += param
                elif param_mode == 0:
                    rb += mem_read(program, param)
                else:
                    rb += mem_read(program, rb + param)
            ip = ip + 2
        elif opcode == 99:
            sys.exit()
        else:
            print("ERROR - OPCODE ", opcode, " NOT VALID")
            sys.exit()


with open('q9input.txt') as f:
    raw = f.readline().split(",")

prog = [int(x) for x in raw]



p = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
p2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
p3 = [104, 1125899906842624, 99]
p4 = [109, -1, 4, 1, 99] #outputs - 1
p5 = [109, -1, 104, 1, 99] #outputs 1
p6 = [109, -1, 204, 1, 99] #outputs 109
p7 = [109, 1, 9, 2, 204, -6, 99] # outputs 204
p8 = [109, 1, 109, 9, 204, -6, 99] #outputs 204
p9 = [109, 1, 209, -1, 204, -106, 99] #outputs 204
p10 = [109, 1, 3, 3, 204, 2, 99] # outputs the input
p11 = [109, 1, 203, 2, 204, 2, 99] #outputs the input

o = compute(p8)
