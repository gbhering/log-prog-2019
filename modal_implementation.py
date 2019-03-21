def findParens(phi):
	i = phi.index('(')
	s = 0
	for j in range(i, len(phi)+1):
		if phi[j] == ')': s-=1
		if phi[j] == '(': s+=1
		if s == 0: return i, j
	raise SyntaxError('Unmatched parens!', phi)

def solve(phi, W, R, V, w):
	phi = phi.replace('(','( ').replace(')', ' )').split()
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
	
	if "NOT" == phi[0]:
		return not sat( phi[1:], W, R, V, w)
	if "SOME" == phi[0]:
		for _w in R[w]:
			if sat( phi[1:], W, R, V, _w ): return True
		return False
	if "ALL" == phi[0]:
		for _w in R[w]:
			if not sat( phi[1:], W, R, V, _w ): return False
		return True
	if '(' in phi:
		i, j = findParens(phi)
		return sat( phi[:i] + [ sat( phi[i+1:j], W, R, V, w) ] + phi[j+1:], W, R, V, w)
	if "AND" in phi:
		i = phi.index('AND')
		return sat( phi[:i], W, R, V, w) and sat( phi[i+1:], W, R, V, w)
	if "OR" in phi:
		i = phi.index('OR')
		return sat( phi[:i], W, R, V, w) or sat( phi[i+1:], W, R, V, w)
	if "->" in phi:
		i = phi.index('->')
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

	phi, w = "p", 's3'
	print("sat(", phi+", M, "+w, ") =>", solve( phi, W, R, V, w ))
	phi, w = "0", 's3'
	print("sat(", phi+", M, "+w, ") =>", solve( phi, W, R, V, w ))
	phi, w = "p AND q", 's3'
	print("sat(", phi+", M, "+w, ") =>", solve( phi, W, R, V, w ))
	phi, w = "p OR q", 's3'
	print("sat(", phi+", M, "+w, ") =>", solve( phi, W, R, V, w ))
	phi, w = "ALL p", 's3'
	print("sat(", phi+", M, "+w, ") =>", solve( phi, W, R, V, w ))
	phi, w = "SOME p", 's3'
	print("sat(", phi+", M, "+w, ") =>", solve( phi, W, R, V, w ))
