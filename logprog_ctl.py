from collections import defaultdict, deque

class Kripke:
	""" K = < S(tates), R(elationships), L(abels) > """
	def __init__(self, S=[], R=[], L={}):
		self.S = set(S)
		self.R = set(R)
		self.L = defaultdict(set).update(L)
		self.SCC = defaultdict(set)

	def checkNOT(phi):
		phi = ' '.join(phi)
		for s in self.S:
			if phi not in L[s]: L[s].add('NOT '+phi)

	def checkIMP(phi1, phi2):
		phi1, phi2 = ' '.join(phi1), ' '.join(phi2)
		for s in self.S:
			if phi1 not in L[s] or phi2 in L[s]: L[s].add(phi1+' IMP '+phi2)

	def checkEX(phi):
		phi = ' '.join(phi)
		for s in [ s for s in self.S if phi in self.L[s] ]:
			for t in [ t for t in self.S if (t,s) in self.R ]:
				self.L[t].add('EX '+phi)

	def checkEU(phi1, phi2):
		phi1, phi2 = ' '.join(phi1), ' '.join(phi2)
		T = [ s for s in self.S if phi2 in self.L[s] ]
		for s in T: self.L[s].add( phi1+' EU '+phi2 )
		while len(T) > 0:
			s = T.pop()
			for t in [ t for t in self.S if (t,s) in self.R ]:
				if phi1+' EU '+phi2 not in self.L[t] and phi1 in self.L[t]:
					self.L[t].add( phi1+' EU '+phi2 )
					T.append(t)

	def _visit(u, unvisited, L):
		if u in unvisited:
			unvisited.pop(unvisited.index(u))
			for v in [ v for v in self.S if (u,v) in self.R ]:
				_visit(v, unvisited, L)
			L.appendleft(u)

	def _assign(u, root, SCCs):
		if u not in SCCs:
			SCCs.update({u, root})
			for v in [ v for v in self.S if (u,v) in self.R ]:
				self._assign(v,root)

	def find_sccs(vertices=self.S):
		""" Kosaraju's algorithm """
		SCCs = dict()
		unvisited = list(self.S)
		L = deque()
		for u in unvisited: self._visit(u, unvisited, L)
		for u in L: self._assign(u,u,SCCs)
		for root in set(SCCs.values()):
			component = { v for v in SCCs.keys() if SCCs[v] == root }
			yield component
			SCCs = { v for v in SCCs if v not in component }


	def checkEG(phi):
		phi = ' '.join(phi)
		Sphi = { s for s in self.S if phi in self.L[s] }
		SCC = [ C for C in self.find_sccs if len(C) > 1 and not Sphi.isdisjoint(C) ]
		T = [s for component in SCC for s in component]
		for s in T: self.L[s].add('EG '+phi)
		while len(T) > 0:
			s = T.pop()
			for t in [ t for t in Sphi if (t,s) in self.R ]:
				if 'EG '+phi not in self.L[t]:
					self.L[t].add('EG '+phi)
					T.append(t)


	def check(phi):
		""" phi is expected to be a list of tokens """
		if len(phi) == 1: return
		if 'NOT' == phi[0]:
			self.check( phi[1:] )
			self.checkNOT( phi[1:] )
		elif 'EG' == phi[0]:
			self.check( phi[1:] )
			self.checkEG( phi[1:] )
		elif 'IMP' in phi:
			i = phi.index('IMP')
			self.check( phi[:i] )
			self.check( phi[i+1:] )
			self.checkIMP( phi[:i], phi[i+1:] )
		elif 'EX' == phi[0]:
			self.check( phi[1:] )
			self.checkEX( phi[1:] )
		elif 'EU' in phi:
			i = phi.index('EU')
			self.check( phi[:i] )
			self.check( phi[i+1:] )
			self.checkEU( phi[:i], phi[i+1:] )
