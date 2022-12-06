import collections

from itertools import islice


def adjacent_digits(n: int) -> bool:
    s = str(n)
    current_digit = s[0]
    for next_digit in s[1:]:
        if current_digit == next_digit:
            return True
        current_digit = next_digit
    return False


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def adjacent_digits2(n: int) -> bool:
    s = str(n)
    current_digit = s[0]

    adjacencies = []
    # Buffer with a 0 as the first digit is not adjacent to
    # a matching digit on the left
    adjacencies.append(0)
    for next_digit in s[1:]:
        # If the current digit matches the next, append 1; else append 0
        if current_digit == next_digit:
            adjacencies.append(1)
        else:
            adjacencies.append(0)
        current_digit = next_digit
    # Buffer with 0 as the last digit is not adjacent to
    # a matching digit on the right
    adjacencies.append(0)

    # If there are exactly two matching digits adjacent to one another,
    # we will see a pattern of (0, 1, 0)
    windows = sliding_window(adjacencies, 3)
    for window in windows:
        if window == (0, 1, 0):
            return True
    return False


def digits_increase(n: int) -> bool:
    s = str(n)
    current_digit = s[0]
    for next_digit in s[1:]:
        if int(next_digit) < int(current_digit):
            return False
        current_digit = next_digit
    return True


assert (
    digits_increase(223450) == False
), "223450 does not meet these criteria (decreasing pair of digits 50)."
assert adjacent_digits(123789) == False, "no double digits"
assert adjacent_digits2(112233) == True
assert adjacent_digits2(123444) == False
assert adjacent_digits2(111122) == True

puzzle_input = range(235741, 706948 + 1)

valid_passwords = []

for n in puzzle_input:
    if adjacent_digits2(n) and digits_increase(n):
        valid_passwords.append(n)

print(len(valid_passwords))
