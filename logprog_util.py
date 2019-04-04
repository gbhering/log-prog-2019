def findParens(phi, st='(', end=')'):
	i = phi.index(st)
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == end: s-=1
		if phi[j] == st: s+=1
		if s == 0: return i, j
	raise SyntaxError('Unmatched parens!', st, end, phi)