from collections import defaultdict

class SATInstance:
	def __init__(self, num_vars, clauses):
		self.num_clauses = len(clauses)
		self.vars = set(range(1, num_vars+1))
		self.clauses = []
		self.clause_list = []
		self.var_clause_map = defaultdict(list)
		for clause in clauses:
			self.add_clause(clause)

	def add_clause(self, cl):
		cl_obj = self.Clause(self, cl, len(self.clause_list))
		self.clause_list.append(cl)
		self.clauses.append(cl_obj)

	def stringify(self):
		st = "Number of variables: " + str(len(self.vars)) + "\n" + \
		"Number of clauses: " + str(self.num_clauses) + "\n" + "Variables: " 

		for i, v in enumerate(self.vars):
			st += str(v)
			if i < len(self.vars) - 1:
				st += ", "
		

		st.strip()
		st += "\n"

		for c in range(len(self.clause_list)):
			st += "Clause " + str(c) + ": " + str(self.clause_list[c]) + "\n"

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




