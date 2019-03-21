def findParensMatch(phi,i):
	s = 0
	for j,v in enumerate(phi[i:]):
		if v == ')': s-=1
		if v == '(':s+=1
		if s == 0: return i+j

def solve(phi, W, R, V, w):
	phi = phi.replace('(','( ').replace(')', ' )').split()
	return sat( phi, W, R, V, w )

def sat( phi, W, R, V, w ):
	# base cases
	if len(phi)==1:
		if phi[0] in V.keys():
			return True if w in V[phi[0]] else False
		if  phi[0] == '0':
			return False
		if  phi[0] == True or phi[0] == False:
			return phi[0]
	elif len(phi)==2: 
		if phi[0] == 'NOT':
			return not sat( [phi[1]], W, R, V, w )
		if phi[0] == 'SOME':
			for _w in R[w]:
				if sat( phi[1:], W, R, V, _w ): return True
			return False
		if phi[0] == 'ALL':
			for _w in R[w]:
				if not sat( phi[1:], W, R, V, _w ): return False
			return True
	elif len(phi)==3:
		if phi[1] == 'AND':
			return sat( [phi[0]], W, R, V, w ) and sat( [phi[2]], W, R, V, w )
		if phi[1] == 'OR':
			return sat( [phi[0]], W, R, V, w ) or sat( [phi[2]], W, R, V, w )
		if phi[1] == '->':
			return not sat( [phi[0]], W, R, V, w ) or sat( [phi[2]], W, R, V, w )
	
	# usual casess, order of cases is priority order as well
	else:
		if  '(' in phi:
			i = phi.index('(')
			j = findParensMatch(phi,i)
			return sat(phi[:i] + [sat(phi[i+1:j],v)] + phi[j+1:], v)
		if  "NOT" in phi:
			i = phi.index('NOT')
			return sat(phi[:i] + [sat(phi[i:i+2], v)] + phi[i+2:], v)
		if "AND" in phi:
			i = phi.index('AND')
			return sat(phi[:i-1] + [sat(phi[i-1:i+2], v)] + phi[i+2:], v)
		if "OR" in phi:
			i = phi.index('OR')
			return sat(phi[:i-1] + [sat(phi[i-1:i+2], v)] + phi[i+2:], v)
		if "->" in phi:
			i = phi.index('->')
			return sat(phi[:i-1] + [sat(phi[i-1:i+2], v)] + phi[i+2:], v)
		if  "SOME" in phi:
			i = phi.index('SOME')
			return sat(phi[:i] + [sat(phi[i:i+2], v)] + phi[i+2:], v)
		if  "ALL" in phi:
			i = phi.index('ALL')
			return sat(phi[:i] + [sat(phi[i:i+2], v)] + phi[i+2:], v)

	# things have failed if we get here
	return phi


if __name__=='__main__':
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
