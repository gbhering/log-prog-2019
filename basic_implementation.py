def findParens(phi):
	i = phi.index('(')
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == ')': s-=1
		if phi[j] == '(': s+=1
		if s == 0: return i, j
	raise SyntaxError('Unmatched parens!', phi)

def solve(phi, V):
	alternates = { 
		'!':'¬', '&':'∧', '|':'v', '->':'→',
		'NOT':'¬', 'OR':'v', 'AND':'∧', 'IMPLIES': '→' 
	}
	for alt, op in alternates.items():
		phi = phi.replace(alt, op)
	for operator in ['¬', '∧', 'v', '→', '(', ')']:
		phi = phi.replace(operator,' '+operator+' ')
	phi = phi.split()
	return rec(phi, V)


# order of cases is also order of priority
def rec(phi, V):
	# some checks to prevent funny errors
	if phi in [True, False]:
		return phi
	if len(phi)==0:
		raise SyntaxError('Malformed expression!', phi)
	if len(phi)==1:
		return phi[0] if phi[0] in [True, False] else V[phi[0]]

	# the actual recursion
	if "¬" == phi[0]:
		return not rec( phi[1:], V )
	if '(' in phi:
		i, j = findParens(phi)
		return rec( phi[:i] + [ rec( phi[i+1:j], V ) ] + phi[j+1:], V )
	if "∧" in phi:
		i = phi.index('∧')
		return rec( phi[:i], V ) and rec( phi[i+1:], V )
	if "v" in phi:
		i = phi.index('v')
		return rec( phi[:i], V ) or rec( phi[i+1:], V )
	if "→" in phi:
		i = phi.index('→')
		return not rec( phi[:i], V ) or rec( phi[i+1:], V )

	# things haVe failed if we get here
	return phi



if __name__=='__main__':
	# for testing purposees
	V = { 'A': True, 'B': False, 'C': False, 'D': True }
	tests = [
		{ 'phi': "A ∧ B", 'result': False },
		{ 'phi': "A v B", 'result' : True },
		{ 'phi': "¬ A", 'result' : False },
		{ 'phi': "A → B", 'result' : False },
		{ 'phi': "B → A", 'result' : True },
		{ 'phi': "( B ∧ A )", 'result' : False },
		{ 'phi': "( B ∧ A ) v ( B ∧ C )", 'result' : False },
		{ 'phi': "( B ∧ A )→( B ∧ C )", 'result' : True },
		{ 'phi': "A v B v C", 'result' : True },
		{ 'phi': "A v B ∧ B v C", 'result' : False },
		{ 'phi': "¬ A v B", 'result' : False },
		{ 'phi': "¬ (A v B)", 'result' : False },
		{ 'phi': "(A→B)→(C→D)", 'result' : True },
		{ 'phi': "(A v B) ∧ (C v D)", 'result' : True },
	]

	for test in tests:
		result = solve(test['phi'], V)
		if result != test['result']: 
			print('Test failed: ', test['phi'], 'resulted in', result)
