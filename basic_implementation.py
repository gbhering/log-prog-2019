def findParensMatch(F,i):
	s = 0
	for j,v in enumerate(F[i:]):
		if v == ')': s-=1
		if v == '(':s+=1
		if s == 0: return i+j

def solve(F, v):
	v[True] = True
	v[False] = False

	F = F.replace('(','( ').replace(')', ' )').split()
	return phi(F, v)


# order of cases is also order of priority
def phi(F, v):
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

	if F[0] == "NOT":
		return not v[F[1]];

	if F[1] == "OR":
		return v[F[0]] or v[F[2]]

	if F[1] == "AND":
		return v[F[0]] and v[F[2]]

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
