from collections import defaultdict

class SATInstance:
	def __init__(self, num_vars, num_clauses):
		self.num_vars = num_vars
		self.num_clauses = num_clauses
		self.vars = set()
		self.clauses = []
		self.clause_list = []
		self.var_clause_map = defaultdict(list)


	def add_variable(self, lit):
		self.vars.add(lit) if lit >= 0 else self.vars.add(-1*lit)

	def add_clause(self, cl):
		cl_obj = self.Clause(self, cl, len(self.clause_list))
		self.clause_list.append(cl)
		self.clauses.append(cl_obj)


	def stringify(self):
		st = "Number of variables: " + str(self.num_vars) + "\n" + 
		"Number of clauses: " + str(self.num_clauses) + "\n" + "Variables: " 

		for v in self.vars:
			st += str(v) + ", "

		st.strip()
		st += "\n"

		for c in range(len(self.clause_list)):
			st += "Clause " + str(c) + ": " + self.clause_list[c].join(" ") + "\n"

		st.strip()
		return st

	class Clause():
		def __init__(self, outer, cl, ind):
			self.ind = ind
			self.outer = outer
			self.cl = cl
			self.un_vars = self.fill_unvars()

		def fill_unvars(self):
			un_vars = set()
			for v in self.cl:
				un_vars.add(v) if v >= 0 else un_vars.add(-1*v)
				self.outer.var_clause_map[v].append(self.ind)








