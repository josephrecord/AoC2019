def expand_write(tup: tuple, i: int, v: int) -> tuple:
    # write a value at an index >= length(tuple)
    # fills with None until desired index
    # e.g. a = (1, 2, 5, 4)
    # expand_write(a, 6, 9) ==> (1, 2, 5, 4, None, None, 9)
    assert type(tup) == tuple, "input must be a tuple"
    assert type(i) == int, "i must be an int"
    assert i >= 0, "index must be positive"
    assert i <= 34463338, "index out of range"
    lst = list(tup)
    length = len(lst)
    if i < length:
        lst[i] = v
    else:
        current_index = length
        while current_index != i:
            lst.append(None)
            current_index += 1
        lst.append(v)
    return tuple(lst)


a = (1, 2, 5, 4)
b = expand_write(a, 1, 9)
c = expand_write(b, 7, 8)

print(c)