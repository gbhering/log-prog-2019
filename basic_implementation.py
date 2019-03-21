def findParens(phi):
	i = phi.index('(')
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == ')': s-=1
		if phi[j] == '(': s+=1
		if s == 0: return i, j
	raise SyntaxError('Unmatched parens!', phi)

def solve(phi, V):
	phi = phi.replace('(','( ').replace(')', ' )').split()
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
	if "NOT" == phi[0]:
		return not rec( phi[1:], V )
	if '(' in phi:
		i, j = findParens(phi)
		return rec( phi[:i] + [ rec( phi[i+1:j], V ) ] + phi[j+1:], V )
	if "AND" in phi:
		i = phi.index('AND')
		return rec( phi[:i], V ) and rec( phi[i+1:], V )
	if "OR" in phi:
		i = phi.index('OR')
		return rec( phi[:i], V ) or rec( phi[i+1:], V )
	if "->" in phi:
		i = phi.index('->')
		return not rec( phi[:i], V ) or rec( phi[i+1:], V )

	# things haVe failed if we get here
	return phi



if __name__=='__main__':
	# for testing purposees
	V = { 'A': True, 'B': False, 'C': False }
	tests = [
		{ 'phi': "A AND B", 'result': False },
		{ 'phi': "A OR B", 'result' : True },
		{ 'phi': "NOT A", 'result' : False },
		{ 'phi': "A -> B", 'result' : False },
		{ 'phi': "B -> A", 'result' : True },
		{ 'phi': "( B AND A )", 'result' : False },
		{ 'phi': "( B AND A ) OR ( B AND C )", 'result' : False },
		{ 'phi': "( B AND A ) -> ( B AND C )", 'result' : True },
		{ 'phi': "A OR B OR C", 'result' : True },
		{ 'phi': "A OR B AND B OR C", 'result' : False },
	]

	for test in tests:
		if solve(test['phi'], V) != test['result']: 
			print('Test failed '+test['phi'])
