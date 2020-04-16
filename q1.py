import time
import math

start_time = time.time()

with open('q1.txt') as f:
    raw = f.readlines()
    dat = list(map(int, raw))

ans1 = []
ans2 = []

# get the fuel for any mass or a quantity of fuel
def get_fuel(i):
    return math.floor(i / 3) - 2


# get the total fuel for a mass
def get_totfuel(i):
    fuels = []
    # first get the fuel required for the mass
    fuels.append(get_fuel(i))
    # calc the fuel cost of fuel, until amt is negative
    # (floor(8/3) - 2) = 0 so stop once the fuel cost is 8 or less
    while fuels[-1] > 9:
        fuels.append(get_fuel(fuels[-1]))
    return sum(fuels)


for i in dat:
    j = get_fuel(i)
    ans1.append(j)

print("Part 1 ans is:", sum(ans1))

for i in dat:
    j = get_totfuel(i)
    ans2.append(j)

print("Part 2 ans is:", sum(ans2))

print((time.time() - start_time), " sec")
