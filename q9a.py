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


a = (1, 2, 5, 4)
b = mem_write(a, 1, 9)
c = mem_write(b, 7, 8)

d = mem_read(c, 7)
e = mem_read(c, 100)

print(a)
print(b)
print(c)
print(d)
print(e)