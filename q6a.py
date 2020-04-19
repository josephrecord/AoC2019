# with open('q6a.txt') as f:
#     raw = f.readlines()

planets = set()

with open('q6a-testinput.txt') as f:
    test_input = f.readlines()
    for line in test_input:
        striped_line = line.rstrip()
        sym_pos = striped_line.find(")")
        planets.add(striped_line[:sym_pos])
        planets.add(striped_line[sym_pos+1:])


print(planets)