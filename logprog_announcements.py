from logprog_multiagent import solve as multiagent_solve

def announce( phi, W, R, V ):
	for w in [ _w for _w in W if not multiagent_solve( phi, W, R, V, _w ) ]:
		W.remove(w)