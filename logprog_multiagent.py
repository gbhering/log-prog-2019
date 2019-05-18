import re
from logprog_util import findParens, preparse

def solve( phi, W, R, V, w ): return sat( preparse(phi), W, R, V, w )

def satDiamond( phi, W, R, V, w ):
	i = phi.index('>')
	agents = phi[1:i:2] if phi[1] != '*' else R.keys()
	for _ag in agents:
		for _w in R[_ag][w]:
			if _w in W and sat( phi[i+1:], W, R, V, _w ): return True
	return False

def satSquare( phi, W, R, V, w ):
	i = phi.index(']')
	agents = phi[1:i:2] if phi[1] != '*' else R.keys()
	for _ag in agents:
		for _w in R[_ag][w]:
			if _w in W and not sat( phi[i+1:], W, R, V, _w ): return False
	return True

def sat( phi, W, R, V, w ):
	# base cases
	if phi == True or phi == [True]: return True
	if phi == False or phi == [False]: return False
	if len(phi)==0: raise SyntaxError('Malformed expression!', phi)
	if len(phi)==1 and phi[0] in V:	return ( w in V[phi[0]] )
	
	if "¬" == phi[0]: return not sat( phi[1:], W, R, V, w )
	if "<" == phi[0]: return satDiamond( phi, W, R, V, w )
	if "[" == phi[0]: return satSquare( phi, W, R, V, w )
	
	if '(' in phi:
		i, j = findParens(phi)
		return sat( phi[:i] + [ sat( phi[i+1:j], W, R, V, w ) ] + phi[j+1:], W, R, V, w )
	
	if "∧" in phi:
		i = phi.index('∧')
		return sat( phi[:i], W, R, V, w ) and sat( phi[i+1:], W, R, V, w )
	if "∨" in phi:
		i = phi.index('∨')
		return sat( phi[:i], W, R, V, w ) or sat( phi[i+1:], W, R, V, w )
	if "→" in phi:
		i = phi.index('→')
		return not sat( phi[:i], W, R, V, w ) or sat( phi[i+1:], W, R, V, w )

	# things have failed if we get here
	raise RuntimeError('Either your expression is malformed or you found a bug!', phi)
