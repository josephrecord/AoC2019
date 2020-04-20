def count_orbits(d, p):
    assert type(p) == str, "plant needs to be a string"
    assert type(d) == dict, "1st arg needs to be dictionary"
    count_orbits.counter += 1
    prev = d.get(p)
    if prev in d:
        return count_orbits(d, prev)
    else:
        return count_orbits.counter


orbitee_list = []
orbiter_list = []

solar_sys = {}

with open('q6a.txt') as f:
    test_input = f.readlines()
    for line in test_input:
        striped_line = line.rstrip() # remove newline char
        sym_pos = striped_line.find(")")
        orbitee = striped_line[:sym_pos]
        orbiter = striped_line[sym_pos+1:]
        # solar_sys.setdefault(orbiter, [])
        solar_sys[orbiter] = orbitee
        orbitee_list.append(orbitee)
        orbiter_list.append(orbiter)
        print(orbiter, " Directly orbits ", orbitee)


planets = set(orbitee_list+orbiter_list)
print("planets len ", len(planets), " :", planets)

print("orbitees ", "len ", len(orbitee_list), orbitee_list, set(orbitee_list))
print("orbiters ", "len ", len(orbiter_list), orbiter_list, set(orbiter_list))

print("solar system: ", solar_sys)

for planet in planets:
    count = 0
    print("planet: ", planet, "- ", solar_sys.get(planet))


count_orbits.counter = 0

for planet in planets:
    print(count_orbits(solar_sys, planet))

ans = count_orbits.counter - 1

print("ans is: ", ans)
