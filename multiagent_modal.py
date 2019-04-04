def findParens(phi, st='(', end=')'):
	i = phi.index(st)
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == end: s-=1
		if phi[j] == st: s+=1
		if s == 0: return i, j
	raise SyntaxError('Unmatched parens!', st, end, phi)

def solve(phi, W, R, V, w):
	alternates = { 
		'!':'¬', '&':'∧', '|':'∨', '->':'→', '[]':'□', '<>':'◇',
		'NOT':'¬', 'OR':'∨', 'AND':'∧', 'IMPLIES':'→', 'NECESSARILY':'□', 'POSSIBLY':'◇' 
	}
	for alt, op in alternates.items():
		phi = phi.replace(alt, op)
	for operator in ['¬', '◇', '□', '∧', '∨', '→', '(', ')']:
		phi = phi.replace(operator,' '+operator+' ')
	phi = phi.split()
	return sat( phi, W, R, V, w )

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


if __name__=='__main__':
	# for testing purposes
	V = { 
		'p': [ 's3', 's4', 's5' ], 
		'q': [ 's1', 's5' ], 
		'r': [ 's1' ] 
	}
	W = [ 's1', 's2', 's3', 's4', 's5'  ]
	R = { 
		's1' : [ 's2', 's3' ], 
		's2' : [ 's5', 's4' ], 
		's3' : [ 's3', 's4' ], 
		's4' : [ 's1', 's5' ], 
		's5' : [ 's5' ] 
	}

	tests = [
		{ 'phi': "q ∧ r", 'w': 's1', 'result': True },
		{ 'phi': "q ∧ r", 'w': 's3', 'result': False },
		{ 'phi': "q ∨ r", 'w': 's3', 'result': False },
		{ 'phi': "p ∨ r", 'w': 's3', 'result': True },
		{ 'phi': "◇ p", 'w': 's3', 'result': True },
		{ 'phi': "◇ p", 'w': 's1', 'result': True },
		{ 'phi': "◇ q", 'w': 's3', 'result': False },
		{ 'phi': "◇ q", 'w': 's1', 'result': False },
		{ 'phi': "□ p", 'w': 's3', 'result': True },
		{ 'phi': "□ ¬q", 'w': 's3', 'result': True },
		{ 'phi': "◇ ¬q", 'w': 's4', 'result': False },
		{ 'phi': "□ ¬r", 'w': 's4', 'result': False },
		{ 'phi': "□ ¬r ∨ q", 'w': 's3', 'result': True },
		{ 'phi': "◇ r ∧ p", 'w': 's4', 'result': False },
	]

	for test in tests:
		result = solve( test['phi'], W, R, V, test['w'] )
		if result != test['result']: 
			print('Test failed: ', test['phi'], 'resulted in', result )

