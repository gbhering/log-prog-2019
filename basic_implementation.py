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
def phi(F, v):
	# base cases
	if len(F)==2 and F[0]=="NOT":
		return not v[F[1]];
	if len(F)==3 and F[1] == "AND":
		return v[F[0]] and v[F[2]]
	if len(F)==3 and F[1]=="OR":
		return v[F[0]] or v[F[2]]
	if len(F)==3 and F[1]=="->":
		return phi([ 'NOT', v[F[0]], 'OR', v[F[2]] ], v)

	if len(F) > 2 and '(' in F:
		i = F.index('(')
		j = findParensMatch(F,i)
		return phi(F[:i] + [phi(F[i+1:j],v)] + F[j+1:], v)

	if len(F) > 2 and "NOT" in F:
		i = F.index('NOT')
		return phi(F[:i] + [phi(F[i:i+2], v)] + F[i+2:], v)

	if len(F) > 3 and "AND" in F:
		i = F.index('AND')
		return phi(F[:i-1] + [phi(F[i-1:i+2], v)] + F[i+2:], v)

	if len(F) > 3 and "OR" in F:
		i = F.index('OR')
		return phi(F[:i-1] + [phi(F[i-1:i+2], v)] + F[i+2:], v)

	if len(F) > 3 and "->" in F:
		i = F.index('->')
		return phi(F[:i-1] + [phi(F[i-1:i+2], v)] + F[i+2:], v)

	# things have failed if we get here
	return F



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
