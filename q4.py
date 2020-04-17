def i(x):
    return int(x)

def s(x):
    return str(x)


fit_criteria = []

for num in range(235741, 706948):
    s = str(num)
    d0 = i(s[0])
    d1 = i(s[1])
    d2 = i(s[2])
    d3 = i(s[3])
    d4 = i(s[4])
    d5 = i(s[5])

    if (d5 >= d4 >= d3 >= d2 >= d1 >= d0) and (d5==d4 or d4==d3 or d3==d2 or d2==d1 or d1==d0):
        fit_criteria.append(num)

print(len(fit_criteria))
