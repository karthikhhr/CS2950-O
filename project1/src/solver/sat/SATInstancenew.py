from collections import defaultdict
import copy
import sys
import random
sys.setrecursionlimit(10000)

class SATInstance:
    def __init__(self, num_vars, clauses):
        self.num_vars = num_vars
        self.clauses = {}
        self.lit_clause_map = defaultdict(list)
        self.unit_clauses = set()
        for clause in clauses:
            self.add_clause(clause)
        self.true_variables = set()

    def add_clause(self, cl):
        index = len(self.clauses)
        cl_obj = self.Clause(self, cl, index)
        self.clauses[index] = cl_obj
        if cl_obj.is_unit():
            self.unit_clauses.add(index)

    def stringify(self):
        st = "Number of variables: " + str((self.num_vars)) + "\n" + \
        "Number of clauses: " + str(len(self.clauses)) + "\n" + "Variables: ["

        for i, v in enumerate(range(1, self.num_vars+1)):
            st += str(v)
            if i < (self.num_vars) - 1:
                st += ", "
        st.strip()
        st += "]\n"

        for c in range(len(self.clauses)):
            st += "Clause " + str(c) + ": " + str(self.clauses[c].cl).replace('set(', '').replace(')', '') + "\n"

        st.strip()
        return st

    def is_SAT(self):
        return len(self.clauses) == 0

    def is_UNSAT(self):
        for ind, clause in self.clauses.items():
            if len(clause.cl) == 0:
                return True
        return False

    def unit_propagate(self):
        while not (len(self.unit_clauses) == 0):
            clause_index = self.unit_clauses.pop()
            if clause_index in self.clauses:
                clause = self.clauses[clause_index]
                if clause.is_unit():
                    lit = list(clause.cl)[0]
                    self.assign_true(lit)
                else:
                    if len(clause.cl) == 0:
                        return "UNSAT" 
                    else:
                        print "YAOZA"
                        del clause
            else:
                print "YIKES"

    def is_pl(self, var):
        num_p = len(self.lit_clause_map[var])
        num_n = len(self.lit_clause_map[var*(-1)])
        if (num_p > 0 and num_n == 0):
            return (True, var)
        elif (num_p == 0 and num_n > 0):
            return (True, var*(-1))
        return (False, None)

    def pure_literal_elem(self):
        for var in range(1, self.num_vars+1):
            is_pure, pure_lit = self.is_pl(var)
            if is_pure:
                self.assign_true(pure_lit)

    def flip(self, p):
        return True if random.random() < p else False

    def choose_literal(self):
        t_max = (None, 0)
        for lit, clauses in self.lit_clause_map.items():
            if len(clauses) > t_max[1]:
                t_max = (lit, len(clauses))
        if t_max[0] is None:
            print "WHOOPS"
            return random.choice(self.lit_clause_map.keys())
        else:
            if self.flip(1.0):
                return t_max[0]
            else:
                return random.choice(self.lit_clause_map.keys())

    def assign_true(self, lit):
        for clause_index in self.lit_clause_map[lit]:
            self.unit_clauses.discard(clause_index)
            self.clauses.pop(clause_index, None)
        for clause_index in self.lit_clause_map[lit*(-1)]:
            if clause_index in self.clauses:
                clause = self.clauses[clause_index]
                clause.cl.discard(lit*(-1))
                if clause.is_unit():
                    self.unit_clauses.add(clause.ind)
        self.lit_clause_map.pop(lit, None)
        self.lit_clause_map.pop(lit*-1, None)
        if lit > 0:
            self.true_variables.add(lit)

    class Clause():
        def __init__(self, outer, cl, ind):
            self.outer = outer
            self.cl = set(cl)
            self.ind = ind
            self.make_lit_mapping()

        def make_lit_mapping(self):
            for lit in self.cl:
                self.outer.lit_clause_map[lit].append(self.ind)

        def is_unit(self):
            return len(self.cl) == 1