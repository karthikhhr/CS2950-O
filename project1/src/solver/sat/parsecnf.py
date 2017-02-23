from SATInstance import *

def read(filename):
    f = open(filename, "r")
    num_vars = 0
    num_clauses = 0
    started_reading = False
    clauses = []
    for line in f:
        if started_reading:
            clause = set()
            for lit in line.split()[:-1]:
                clause.add(int(lit))
            if len(clause) > 0:
                clauses.append(clause)
        if not started_reading and line.split()[0] == 'p':
            started_reading = True
            num_vars = int(line.split()[2])
            num_clauses = int(line.split()[3])
    return num_vars, clauses

num_vars, clauses = read("C169_FV.cnf")
problem = SATInstance(num_vars, clauses)
print problem.stringify()
print problem.stringify()

def DPLL(problem):
    if problem.is_SAT():
        return True
    if problem.is_UNSAT():
        return False
    problem.unit_propagate()
    problem.pure_literal_elem()
    lit = problem.choose_literal()
    problem1 = copy.deepcopy(problem)
    problem2 = copy.deepcopy(problem)
    problem1.assign_true(lit)
    problem2.assign_true(lit*(-1))
    return DPLL(problem1) or DPLL(problem2)

print DPLL(problem)
