from logprog_multiagent import solve as multiagent_solve

def announce( phi, W, R, V ):
	return [ _w for _w in W if multiagent_solve( phi, W, R, V, _w ) ]

def make_transitive( R ):
	pass

def make_reflexive( R ):
	for agent, states in R.items():
		for state, edges in states.items():
			edges.append(state)

def make_euclidean( R ):
	make_transitive(R)
	make_reflexive(R)
