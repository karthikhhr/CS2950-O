def read(filename):
    f = open("input/simple.cnf", "r")
    num_vars = 0
    num_clauses = 0
    started_reading = False
    clauses = []
    for line in f:
        if started_reading:
            clause = set()
            for lit in line.split()[:-1]:
                clause.add(int(lit))
            clauses.append(clause)
        if line.split()[0] == 'p':
            started_reading = True
            num_vars = int(line.split()[2])
            num_clauses = int(line.split()[3])
    return num_vars, clauses