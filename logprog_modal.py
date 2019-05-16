from logprog_util import findParens, preparse

def solve( phi, W, R, V, w ): return sat( preparse(phi), W, R, V, w )

def sat( phi, W, R, V, w ):
	if phi in [True, False]:
		return phi
	if len(phi)==0:
		raise SyntaxError('Malformed expression!', phi)
	if len(phi)==1:
		if phi[0] in V:
			return True if w in V[phi[0]] else False
		if  phi[0] == '0':
			return False
		if  phi[0] == True or phi[0] == False:
			return phi[0]
	
	if "¬" == phi[0]:
		return not sat( phi[1:], W, R, V, w)
	if "◇" == phi[0]:
		for _w in R[w]:
			if sat( phi[1:], W, R, V, _w ): return True
		return False
	if "□" == phi[0]:
		for _w in R[w]:
			if not sat( phi[1:], W, R, V, _w ): return False
		return True
	if '(' in phi:
		i, j = findParens(phi)
		return sat( phi[:i] + [ sat( phi[i+1:j], W, R, V, w) ] + phi[j+1:], W, R, V, w)
	if "∧" in phi:
		i = phi.index('∧')
		return sat( phi[:i], W, R, V, w) and sat( phi[i+1:], W, R, V, w)
	if "∨" in phi:
		i = phi.index('∨')
		return sat( phi[:i], W, R, V, w) or sat( phi[i+1:], W, R, V, w)
	if "→" in phi:
		i = phi.index('→')
		return not sat( phi[:i], W, R, V, w) or sat( phi[i+1:], W, R, V, w)

	# things have failed if we get here
	return phi
