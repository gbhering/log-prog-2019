	def _visit(u, unvisited, L, edges):
		if u in unvisited:
			unvisited.remove(u)
			for v in [ v for v in unvisited if (u,v) in edges ]:
				_visit(v, unvisited, L, edges)
			L.appendleft(u)

	def _assign(u, root, roots, vertices, edges):
		if u not in roots:
			roots.update({u, root})
			for v in [ v for v in vertices if (u,v) in edges ]:
				_assign(v,root)

	def find_sccs(vertices, edges):
		""" Kosaraju's algorithm """
		roots = dict()
		unvisited = set(vertices)
		L = deque()
		for u in unvisited: _visit(u, unvisited, L, edges)
		for u in L: _assign(u,u,roots)
		for root in set(roots.values()):
			component = { v for v in roots.keys() if roots[v] == root }
			yield component
			roots = { v for v in roots if v not in component }

