from collections import defaultdict
import copy
import sys
import random
sys.setrecursionlimit(10000)

class SATInstance:
	def __init__(self, num_vars, clauses):
		self.num_clauses = len(clauses)
		self.vars = set(range(1, num_vars+1))
		self.clauses = {}
		self.lit_clause_map = defaultdict(list)
		for clause in clauses:
			self.add_clause(clause)
		self.true_variables = set()

	def add_clause(self, cl):
		index = len(self.clauses)
		cl_obj = self.Clause(self, cl, index)
		self.clauses[index] = cl_obj

	def stringify(self):
		st = "Number of variables: " + str(len(self.vars)) + "\n" + \
		"Number of clauses: " + str(self.num_clauses) + "\n" + "Variables: " 

		for i, v in enumerate(self.vars):
			st += str(v)
			if i < len(self.vars) - 1:
				st += ", "
		st.strip()
		st += "\n"

		for c in range(len(self.clauses)):
			st += "Clause " + str(c) + ": " + str(self.clauses[c].cl) + "\n"

		st.strip()
		return st

	def is_SAT(self):
		for ind, clause in self.clauses.items():
			if not clause.is_consistent():
				return False
		return True

	def is_UNSAT(self):
		for ind, clause in self.clauses.items():
			if len(clause.cl) == 0:
				return True
		return False

	def unit_propagate(self):
		current_clauses = copy.copy(self.clauses)
		for ind, clause in current_clauses.items():
			if clause.is_unit():
				lit = list(clause.cl)[0]
				for clause_index in self.lit_clause_map[lit]:
					self.clauses.pop(clause_index, None)
				for clause_index in self.lit_clause_map[lit*(-1)]:
					if clause_index in self.clauses:
						self.clauses[clause_index].cl.discard(lit*(-1))
						self.clauses[clause_index].n_f += 1
				self.lit_clause_map.pop(lit, None)
				self.lit_clause_map.pop(lit*(-1), None)
				if lit > 0:
					self.true_variables.add(lit)
				self.clauses.pop(ind, "None")
		del current_clauses

	def is_pl(self, var):
		num_p = len(self.lit_clause_map[var])
		num_n = len(self.lit_clause_map[var*(-1)])
		if (num_p > 0 and num_n == 0):
			return (True, var)
		elif (num_p == 0 and num_n > 0):
			return (True, var*(-1))
		return (False, None)

	def pure_literal_elem(self):
		for var in self.vars:
			is_pure, pure_lit = self.is_pl(var)
			if is_pure:
				for clause_index in self.lit_clause_map[pure_lit]:
					self.clauses.pop(clause_index, None)
				for clause_index in self.lit_clause_map[pure_lit*(-1)]:
					if clause_index in self.clauses:
						self.clauses[clause_index].cl.discard[pure_lit*(-1)]
						self.clauses[clause_index].n_f += 1
				del self.lit_clause_map[pure_lit]
				del self.lit_clause_map[pure_lit*(-1)]
				self.add_clause([pure_lit])
				if pure_lit > 0:
					self.true_variables.add(pure_lit)

	def choose_literal(self):
		t_max = (None, 0)
		for lit, clauses in self.lit_clause_map.items():
			if len(clauses) > t_max[1]:
				t_max = (lit, len(clauses))
		if t_max[0] == None:
			return random.choice(self.lit_clause_map.keys())
		else:
			return t_max[0]

	def assign_true(self, lit):
		for clause_index in self.lit_clause_map[lit]:
			self.clauses.pop(clause_index, None)
		for clause_index in self.lit_clause_map[lit*(-1)]:
			if clause_index in self.clauses:
				self.clauses[clause_index].cl.discard(lit*(-1))
				self.clauses[clause_index].n_f += 1
			self.lit_clause_map.pop(lit, None)
			self.lit_clause_map.pop(lit*(-1), None)
			if lit > 0:
				self.true_variables.add(lit)

	class Clause():
		def __init__(self, outer, cl, ind):
			self.outer = outer
			self.cl = set(cl)
			self.ind = ind
			self.n_t = 0 
			self.n_f = 0
			self.og_len = len(self.cl)
			self.make_lit_mapping()

		def make_lit_mapping(self):
			for lit in self.cl:
				self.outer.lit_clause_map[lit].append(self.ind)

		def is_consistent(self):
			return (self.n_t >= 1)

		def is_unit(self):
			if self.n_f == self.og_len - 1 and self.n_t == 0:
				return True
			return False
