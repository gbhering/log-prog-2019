from logprog_basic import solve as basic_solve
from logprog_modal import solve as modal_solve
from logprog_multiagent import solve as multiagent_solve
from logprog_announcements import announce


def respond_waiter( ag, W, R, V, w ):
	if multiagent_solve( '<{0}> 1a ^ 1b ^ 1c'.format(ag.lower()), W, R, V, w ):
		announce( '<{0}> 1a ^ 1b ^ 1c'.format(ag.lower()), W, R, V )
		if multiagent_solve( '[{0}] 1a ^ 1b ^ 1c'.format(ag.lower()), W, R, V, w ):
			announce( '[{0}] 1a ^ 1b ^ 1c'.format(ag.lower()), W, R, V )
			print( "{0}: Yes, please.".format(ag) )
		else:
			announce( '¬[{0}] 1a ^ 1b ^ 1c'.format(ag.lower()), W, R, V )
			print( "{0}: Maybe...".format(ag) )
	else:
		print( "{0}: No, thank you.".format(ag) )


def test_announcements():
	W = [ '000', '010', '100', '110', '001', '011', '101', '111' ]
	V = { '0a' : [ w for w in W if w[0] == '0' ], '1a' : [ w for w in W if w[0] == '1' ],
		  '0b' : [ w for w in W if w[1] == '0' ], '1b' : [ w for w in W if w[1] == '1' ],
		  '0c' : [ w for w in W if w[2] == '0' ], '1c' : [ w for w in W if w[2] == '1' ], }
	R = { 'ana' : { w :[ _w for _w in W if _w[0] == w[0] ] for w in W },
		  'bea' : { w :[ _w for _w in W if _w[1] == w[1] ] for w in W },
		  'cal' : { w :[ _w for _w in W if _w[2] == w[2] ] for w in W }, }
	w = '111'

	print( 'Announcement test: Do you all want coffee?' ) 
	respond_waiter( 'Ana', W, R, V, w )
	respond_waiter( 'Bea', W, R, V, w )
	respond_waiter( 'Cal', W, R, V, w )


def test_multiagent():
	V = { 
		'p': [ 's3', 's4', 's5' ], 
		'q': [ 's1', 's5' ], 
		'r': [ 's1' ] 
	}
	W = [ 's1', 's2', 's3', 's4', 's5'  ]
	R = { 
		'ana' : {
			's1' : [ 's2', 's3' ], 
			's2' : [ 's5', 's4' ], 
			's3' : [ 's3', 's4' ], 
			's4' : [ 's1', 's5' ], 
			's5' : [ 's5' ],
		},
		'bea' : {
			's1' : [ ], 
			's2' : [ ], 
			's3' : [ ], 
			's4' : [ ], 
			's5' : [ ],
		},
	}

	tests = [
		{ 'phi': "q ∧ r", 'w': 's1', 'result': True },
		{ 'phi': "q ∧ r", 'w': 's3', 'result': False },
		{ 'phi': "q ∨ r", 'w': 's3', 'result': False },
		{ 'phi': "p ∨ r", 'w': 's3', 'result': True },
		{ 'phi': "[*]p ∨ r", 'w': 's2', 'result': True },
		{ 'phi': "<*>q ∨ r", 'w': 's2', 'result': True },
		{ 'phi': "[ana]p ∨ r", 'w': 's1', 'result': False },
		{ 'phi': "<ana,bea>¬p", 'w': 's2', 'result': False },
		{ 'phi': "[bea]¬p", 'w': 's2', 'result': True },
		{ 'phi': "[bea]¬p", 'w': 's2', 'result': True },
		{ 'phi': "[ana](¬p) v p", 'w': 's2', 'result': True },
		{ 'phi': "[ana]((¬p) v p)", 'w': 's2', 'result': True },
	]

	failed = False
	for test in tests:
		try:
			result = multiagent_solve( test['phi'], W, R, V, test['w'] )
		except Exception as e:
			print( e, test['phi'] )
			failed = True
		if result != test['result']: 
			failed = True
			print('Test failed: ', test['phi'], 'resulted in', result )

	if not failed: print('All multiagent tests passed!')

def test_modal():
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

	tests = [
		{ 'phi': "q ∧ r", 'w': 's1', 'result': True },
		{ 'phi': "q ∧ r", 'w': 's3', 'result': False },
		{ 'phi': "q ∨ r", 'w': 's3', 'result': False },
		{ 'phi': "p ∨ r", 'w': 's3', 'result': True },
		{ 'phi': "◇ p", 'w': 's3', 'result': True },
		{ 'phi': "◇ p", 'w': 's1', 'result': True },
		{ 'phi': "◇ q", 'w': 's3', 'result': False },
		{ 'phi': "◇ q", 'w': 's1', 'result': False },
		{ 'phi': "□ p", 'w': 's3', 'result': True },
		{ 'phi': "□ ¬q", 'w': 's3', 'result': True },
		{ 'phi': "◇ ¬q", 'w': 's4', 'result': False },
		{ 'phi': "□ ¬r", 'w': 's4', 'result': False },
		{ 'phi': "□ ¬r ∨ q", 'w': 's3', 'result': True },
		{ 'phi': "◇ r ∧ p", 'w': 's4', 'result': False },
	]

	failed = False
	for test in tests:
		result = modal_solve( test['phi'], W, R, V, test['w'] )
		if result != test['result']: 
			print('Test failed: ', test['phi'], 'resulted in', result )
			failed = True

	if not failed: print("All modal tests passed!")

def test_basic():
	V = { 'A': True, 'B': False, 'C': False, 'D': True }
	tests = [
		{ 'phi': "A ∧ B", 'result': False },
		{ 'phi': "A v B", 'result' : True },
		{ 'phi': "¬ A", 'result' : False },
		{ 'phi': "A → B", 'result' : False },
		{ 'phi': "B → A", 'result' : True },
		{ 'phi': "( B ∧ A )", 'result' : False },
		{ 'phi': "( B ∧ A ) v ( B ∧ C )", 'result' : False },
		{ 'phi': "( B ∧ A )→( B ∧ C )", 'result' : True },
		{ 'phi': "A v B v C", 'result' : True },
		{ 'phi': "A v B ∧ B v C", 'result' : False },
		{ 'phi': "¬ A v B", 'result' : False },
		{ 'phi': "¬ (A v B)", 'result' : False },
		{ 'phi': "(A→B)→(C→D)", 'result' : True },
		{ 'phi': "(A v B) ∧ (C v D)", 'result' : True },
	]

	failed = False
	for test in tests:
		result = basic_solve(test['phi'], V)
		if result != test['result']: 
			failed = True
			print('Test failed: ', test['phi'], 'resulted in', result)

	if not failed: print("All basic tests passed!")

if __name__=='__main__':
	test_basic()
	test_modal()
	test_multiagent()
	test_announcements()
