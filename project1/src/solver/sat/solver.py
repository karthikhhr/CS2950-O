from SATInstancenew import *
import sys
import time

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

args = sys.argv
num_vars, clauses = read(args[1])
instance_name = args[1].split('/')[-1]
problem = SATInstance(num_vars, clauses)

def dpll(prob):
    if prob.unit_propagate():
        return None
    prob.pure_literal_elem()
    if prob.is_SAT():
        return prob.true_variables
    if prob.is_UNSAT():
        return None
    lit = prob.choose_literal()
    problem1 = copy.deepcopy(prob)
    problem2 = copy.deepcopy(prob)
    problem1.assign_true(lit)
    problem2.assign_true(lit*(-1))
    return dpll(problem1) or dpll(problem2)


# def dpll_iterative(prob):
#     rec_stack = [prob]
#     visited = set()
#     while len(rec_stack):
#         problem = rec_stack.pop()
#         if problem.is_UNSAT():
#             continue
#         if problem not in visited:
#             visited.add(problem)
#             lit = problem.choose_literal()
#             prob1 = copy.deepcopy(problem)
#             prob2 = copy.deepcopy(problem)
#             prob1.assign_true(lit)
#             prob2.assign_true(lit*(-1))
#             rec_stack.append(prob1)
#             rec_stack.append(prob2)
#         if problem.is_SAT():
#             return problem.true_variables
#     return None


start = time.time()
true_vars = dpll(problem)
end = time.time()
time = end-start
time = float("{0:.2f}".format(time))
res_string = 'UNSAT'

if true_vars:
    false_vars = set(range(1, problem.num_vars+1)) - true_vars
    res_string = "SAT Solution: "
    for ti in sorted(list(true_vars)):
        res_string += str(ti) + " true "
    for fi in sorted(list(false_vars)):
        res_string += str(fi) + " false "
    res_string.strip()

print "Instance: " + instance_name + " Time: " + str(time) + " Result: " + res_string
