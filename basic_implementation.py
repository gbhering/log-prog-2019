def findParensMatch(F,i):
	s = 0
	for j,v in enumerate(F[i:]):
		if v == ')': s-=1
		if v == '(':s+=1
		if s == 0: return i+j

def solve(F, db):
	db[True] = True
	db[False] = False

	F = F.split(' ')
	return phi(F, db)


# order of cases is also order of priority
def phi(F, db):
	if len(F) > 2 and '(' in F:
		i = F.index('(')
		j = findParensMatch(F,i)
		return phi(F[:i] + [phi(F[i+1:j],db)] + F[j+1:], db)

	if len(F) > 2 and "NOT" in F:
		i = F.index('NOT')
		return phi(F[:i] + [phi(F[i:i+2], db)] + F[i+2:], db)

	if len(F) > 3 and "AND" in F:
		i = F.index('AND')
		return phi(F[:i-1] + [phi(F[i-1:i+2], db)] + F[i+2:], db)

	if len(F) > 3 and "OR" in F:
		i = F.index('OR')
		return phi(F[:i-1] + [phi(F[i-1:i+2], db)] + F[i+2:], db)

	if F[0] == "NOT":
		return not db[F[1]];

	if F[1] == "OR":
		return db[F[0]] or db[F[2]]

	if F[1] == "AND":
		return db[F[0]] and db[F[2]]

	return F



if __name__=='__main__':
	db = { 'A': True, 'B': False, 'C': False }
	print("DB:", db)

	F = "A AND B"
	print(F, '=>', solve(F, db))

	F = "A OR B"
	print(F, '=>', solve(F, db))

	F = "NOT A"
	print(F, '=>', solve(F, db))

	F = "A OR NOT B OR C"
	print(F, '=>', solve(F, db))

	F = "NOT A AND NOT B OR NOT C"
	print(F, '=>', solve(F, db))

	F = "NOT A OR B OR C"
	print(F, '=>', solve(F, db))

	F = "NOT ( A OR B OR C )"
	print(F, '=>', solve(F, db))

	F = "NOT ( A OR B OR C ) OR A"
	print(F, '=>', solve(F, db))
