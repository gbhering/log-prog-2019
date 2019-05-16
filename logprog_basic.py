from logprog_util import findParens, preparse

def solve( phi, V ): return rec( preparse(phi), V )

# order of cases is also order of priority
def rec( phi, V ):
	# some checks to prevent funny errors
	if phi in [True, False]:
		return phi
	if len(phi)==0:
		raise SyntaxError('Malformed expression!', phi)
	if len(phi)==1:
		return phi[0] if phi[0] in [True, False] else V[phi[0]]

	# the actual recursion
	if "¬" == phi[0]:
		return not rec( phi[1:], V )
	if '(' in phi:
		i, j = findParens(phi)
		return rec( phi[:i] + [ rec( phi[i+1:j], V ) ] + phi[j+1:], V )
	if "∧" in phi:
		i = phi.index('∧')
		return rec( phi[:i], V ) and rec( phi[i+1:], V )
	if "∨" in phi:
		i = phi.index('∨')
		return rec( phi[:i], V ) or rec( phi[i+1:], V )
	if "→" in phi:
		i = phi.index('→')
		return not rec( phi[:i], V ) or rec( phi[i+1:], V )

	# things have failed if we get here
	return phi