import re

def findParens(phi, st='(', end=')'):
	i = phi.index(st)
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == end: s-=1
		if phi[j] == st: s+=1
		if s == 0: return i, j
	raise SyntaxError('Unmatched parens!', st, end, phi)

def solve( phi, W, R, V, w ):
	alternates = { 
		'^':'∧', 'v':'∨',
		'!':'¬', '&':'∧', '|':'∨', '->':'→',
		'NOT':'¬', 'OR':'∨', 'AND':'∧', 'IMPLIES':'→',
	}
	for alt, op in alternates.items():
		phi = phi.replace(alt, op)
	phi = re.sub(r'¬([a-zA-Z]+)', r'(¬\1)', phi)
	for operator in ['¬', '◇', '□', '∧', '∨', '→', '(', ')', '<', '>', '[', ']', ',']:
		phi = phi.replace(operator,' '+operator+' ')
	phi = phi.split()
	return sat( phi, W, R, V, w )

def satDiamond( phi, W, R, V, w ):
	i = phi.index('>')
	agents = phi[1:i:2] if phi[1] != '*' else R.keys()
	for _ag in agents:
		for _w in R[_ag][w]:
			if sat( phi[i+1:], W, R, V, _w ): return True
	return False

def satSquare( phi, W, R, V, w ):
	i = phi.index(']')
	agents = phi[1:i:2] if phi[1] != '*' else R.keys()
	for _ag in agents:
		for _w in R[_ag][w]:
			if not sat( phi[i+1:], W, R, V, _w ): return False
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


if __name__=='__main__':
	# for testing purposes
	V = { 
		'p': [ 's3', 's4', 's5' ], 
		'q': [ 's1', 's5' ], 
		'r': [ 's1' ] 
	}
	W = [ 's1', 's2', 's3', 's4', 's5'  ]
	R = { 
		'ana' : {
			's1' : [ 's2', 's3' ], 
			's2' : [ 's5', 's4' ], 
			's3' : [ 's3', 's4' ], 
			's4' : [ 's1', 's5' ], 
			's5' : [ 's5' ],
		},
		'bea' : {
			's1' : [ ], 
			's2' : [ ], 
			's3' : [ ], 
			's4' : [ ], 
			's5' : [ ],
		},
	}

	tests = [
		{ 'phi': "q ∧ r", 'w': 's1', 'result': True },
		{ 'phi': "q ∧ r", 'w': 's3', 'result': False },
		{ 'phi': "q ∨ r", 'w': 's3', 'result': False },
		{ 'phi': "p ∨ r", 'w': 's3', 'result': True },
		{ 'phi': "[]p ∨ r", 'w': 's2', 'result': True },
		{ 'phi': "<*>q ∨ r", 'w': 's2', 'result': True },
		{ 'phi': "[ana]p ∨ r", 'w': 's1', 'result': False },
		{ 'phi': "<ana,bea>¬p", 'w': 's2', 'result': False },
		{ 'phi': "[bea]¬p", 'w': 's2', 'result': True },
		{ 'phi': "[bea]¬p", 'w': 's2', 'result': True },
		{ 'phi': "[ana](¬p) v p", 'w': 's2', 'result': True },
		{ 'phi': "[ana](¬p v p)", 'w': 's2', 'result': True },
	]

	failed = False
	for test in tests:
		result = solve( test['phi'], W, R, V, test['w'] )
		if result != test['result']: 
			failed = True
			print('Test failed: ', test['phi'], 'resulted in', result )

	if not failed: print('All tests passed!')
