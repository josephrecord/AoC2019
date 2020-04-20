
# def first_common_anncestor(d, p1, p2):
#     p1_ancestors = []
#     p2_ancestors = []
#     p1_ancestors.append(prev_planet(d, p1))
#     p2_ancestors.append(prev_planet(d, p2))


def list_ancestors(d, p, a):
    prev = d.get(p)
    if prev is None:
        return a
    else:
        a.append(prev)
        return list_ancestors(d, prev, a)


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
        #solar_sys.setdefault(orbitee, [])
        solar_sys[orbiter] = orbitee
        orbitee_list.append(orbitee)
        orbiter_list.append(orbiter)
        print(orbiter, " Directly orbits ", orbitee)


planets = set(orbitee_list+orbiter_list)
print("planets len ", len(planets), " :", planets)

print("orbitees ", "len ", len(orbitee_list), orbitee_list, set(orbitee_list))
print("orbiters ", "len ", len(orbiter_list), orbiter_list, set(orbiter_list))

print("solar system: ", solar_sys)

# print(prev_planet(solar_sys, 'SAN'))
# print(prev_planet(solar_sys, 'YOU'))

you_ancestors = []
san_ancestors = []

print("YOU's ancestors ", list_ancestors(solar_sys, 'YOU', you_ancestors))
print("SAN's ancestors ", list_ancestors(solar_sys, 'SAN', san_ancestors))

for preceding_planet in you_ancestors:
    if preceding_planet in san_ancestors:
        common_ancestor = preceding_planet
        location = you_ancestors.index(common_ancestor)
        print("found: ", common_ancestor)
        print("index: ", location)
        break
    else:
        #print(preceding_planet, " not in SAN_AN")
        pass

for preceding_planet in san_ancestors:
    if preceding_planet in you_ancestors:
        common_ancestor2 = preceding_planet
        location2 = san_ancestors.index(common_ancestor2)
        print("found: ", common_ancestor2)
        print("index: ", location2)
        break
    else:
        #print(preceding_planet, " not in YOU_AN")
        pass

print(location+location2)