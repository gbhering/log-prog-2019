def findParensMatch(f,i):
	s = 0
	for j,v in enumerate(f[i:]):
		if v == ')': s-=1
		if v == '(':s+=1
		if s == 0: return i+j

def solve(f, v):
	v[True] = True
	v[False] = False

	f = f.replace('(','( ').replace(')', ' )').split()
	return phi(f, v)


# let us define W set of possible worlds
# let us define R as the set of binary relations
# between w' and w", members of W
# let us define F = (W, R) as the graph in which 
# formulas are evaluated

# let us define M = (F,V)

# order of cases is also order of priority
def phi(f, v):
	# base cases
	if len(f)==2 and f[0]=="NOT":
		return not v[f[1]];
	if len(f)==3 and f[1] == "AND":
		return v[f[0]] and v[f[2]]
	if len(f)==3 and f[1]=="OR":
		return v[f[0]] or v[f[2]]
	if len(f)==3 and f[1]=="->":
		return phi([ 'NOT', v[f[0]], 'OR', v[f[2]] ], v)

	if len(f) > 2 and '(' in f:
		i = f.index('(')
		j = findParensMatch(f,i)
		return phi(f[:i] + [phi(f[i+1:j],v)] + f[j+1:], v)

	if len(f) > 2 and "NOT" in f:
		i = f.index('NOT')
		return phi(f[:i] + [phi(f[i:i+2], v)] + f[i+2:], v)

	if len(f) > 3 and "AND" in f:
		i = f.index('AND')
		return phi(f[:i-1] + [phi(f[i-1:i+2], v)] + f[i+2:], v)

	if len(f) > 3 and "OR" in f:
		i = f.index('OR')
		return phi(f[:i-1] + [phi(f[i-1:i+2], v)] + f[i+2:], v)

	if len(f) > 3 and "->" in f:
		i = f.index('->')
		return phi(f[:i-1] + [phi(f[i-1:i+2], v)] + f[i+2:], v)

	# things have failed if we get here
	return f



if __name__=='__main__':
	v = { 'A': True, 'B': False, 'C': False }
	print("v:", v)

	f = "A AND B"
	print(f, '=>', solve(f, v))

	f = "A OR B"
	print(f, '=>', solve(f, v))

	f = "NOT A"
	print(f, '=>', solve(f, v))

	f = "A OR NOT B OR C"
	print(f, '=>', solve(f, v))

	f = "NOT A AND NOT B OR NOT C"
	print(f, '=>', solve(f, v))

	f = "NOT A OR B OR C"
	print(f, '=>', solve(f, v))

	f = "NOT (A OR B OR C)"
	print(f, '=>', solve(f, v))

	f = "NOT (A OR B OR C) OR A"
	print(f, '=>', solve(f, v))

	f = "(A -> C)"
	print(f, '=>', solve(f, v))

	f = "(C -> A)"
	print(f, '=>', solve(f, v))

	f = "(A -> A)"
	print(f, '=>', solve(f, v))

	f = "(B -> C)"
	print(f, '=>', solve(f, v))
