import re

def findParens(phi, st='(', end=')'):
	i = phi.index(st)
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == end: s-=1
		elif phi[j] == st: s+=1
		if s == 0: return i, j
	raise SyntaxError('Unmatched parens!', st, end, phi)

def preparse( phi ):
	alternates = { 
		'^':'∧', 'v':'∨',
		'!':'¬', '&':'∧', '|':'∨', '->':'→', '[]':'□', '<>':'◇',
		'NOT':'¬', 'OR':'∨', 'AND':'∧', 'IMPLIES':'→', 'NECESSARILY':'□', 'POSSIBLY':'◇' 
	}
	for alt, op in alternates.items():
		phi = phi.replace(alt, op)
	# phi = re.sub(r'¬([a-zA-Z]+)', r'(¬\1)', phi)
	for operator in ['¬', '◇', '□', '∧', '∨', '→', '(', ')', '<', '>', '[', ']', ',']:
		phi = phi.replace(operator,' '+operator+' ')
	phi = phi.split()
	return phi


def make_transitive( R ):
	pass

def make_reflexive( R ):
	for agent, states in R.items():
		for state, edges in states.items():
			edges.append(state)

def make_euclidean( R ):
	make_transitive(R)
	make_reflexive(R)
