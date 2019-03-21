def findParens(phi):
	i = phi.index('(')
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == ')': s-=1
		if phi[j] == '(': s+=1
		if s == 0: return i, j
	
	raise SyntaxError('Unmatched parens!', phi)

def solve(phi, V):
	V[True] = True
	V[False] = False

	phi = phi.replace('(','( ').replace(')', ' )').split()
	return rec(phi, V)


# order of cases is also order of priority
def rec(phi, V):
	if len(phi)==0:
		raise SyntaxError('Malformed expression!', phi)
	if len(phi)==1:
		return V[phi[0]]
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
	if "NOT" == phi[0]:
		return not rec( phi[1], V )

	# things haVe failed if we get here
	return phi



if __name__=='__main__':
	v = { 'A': True, 'B': False, 'C': False }
	print("v:", v)

	F = "A AND B"
	print(F, '=>', solve(F, v))

	F = "A OR B"
	print(F, '=>', solve(F, v))

	F = "NOT A"
	print(F, '=>', solve(F, v))

	F = "A OR NOT B OR C"
	print(F, '=>', solve(F, v))

	F = "NOT A AND NOT B OR NOT C"
	print(F, '=>', solve(F, v))

	F = "NOT A OR B OR C"
	print(F, '=>', solve(F, v))

	F = "NOT (A OR B OR C)"
	print(F, '=>', solve(F, v))

	F = "NOT (A OR B OR C) OR A"
	print(F, '=>', solve(F, v))

	F = "(A -> C)"
	print(F, '=>', solve(F, v))

	F = "(C -> A)"
	print(F, '=>', solve(F, v))

	F = "(A -> A)"
	print(F, '=>', solve(F, v))

	F = "(B -> C)"
	print(F, '=>', solve(F, v))
