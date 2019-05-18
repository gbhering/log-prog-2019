from logprog_basic import solve as basic_solve
from logprog_modal import solve as modal_solve
from logprog_multiagent import solve as multiagent_solve
from logprog_announcements import announce, make_euclidean

def e(ag, st, W):
	if ag == 'ana': return [ w for w in W if st[0] == w[0] ]
	if ag == 'bea': return [ w for w in W if st[1] == w[1] ]
	if ag == 'cal': return [ w for w in W if st[2] == w[2] ]

def test_announcements():
	V = {
		'0a' : [ '000', '010', '001', '011' ],
		'1a' : [ '100', '110', '101', '111' ],
		'0b' : [ '100', '100', '101', '101' ],
		'1b' : [ '010', '110', '011', '111' ],
		'0c' : [ '000', '010', '100', '110' ],
		'1c' : [ '001', '011', '101', '111' ],
	}
	W = [ '000', '010', '100', '110', '001', '011', '101', '111' ]
	R = {
		'ana' : { 
			'000': e('ana','000', W), '010': e('ana','010', W), '100': e('ana','100', W), '110': e('ana','110', W), 
			'001': e('ana','001', W), '011': e('ana','011', W), '101': e('ana','101', W), '111': e('ana','111', W), 
		},
		'bea' : { 
			'000': e('bea','000', W), '100': e('bea','100', W), '010': e('bea','010', W), '110': e('bea','110', W),
			'001': e('bea','001', W), '101': e('bea','101', W), '011': e('bea','011', W), '111': e('bea','111', W),
		},
		'cal' : { 
			'000': e('cal','000', W), '100': e('cal','100', W), '010': e('cal','010', W), '110': e('cal','110', W),
			'001': e('cal','001', W), '101': e('cal','101', W), '011': e('cal','011', W), '111': e('cal','111', W),
		},
	}
	w = '111'

	make_euclidean(R)
	print( 'Announcement test: Do you all want coffee?' ) 
	
	answer = "Maybe" if multiagent_solve( '<ana> 1a ^ 1b ^ 1c', W, R, V, w ) else "No"
	print( 'Ana:', answer )
	W = announce( '<ana> 1a ^ 1b ^ 1c', W, R, V ) if answer == "Maybe" else announce( '¬<ana> 1a ^ 1b ^ 1c', W, R, V )
	
	answer = "Maybe" if multiagent_solve( '<bea> 1a ^ 1b ^ 1c', W, R, V, w ) else "No"
	print( 'Bea:', answer )
	W = announce( '<bea> 1a ^ 1b ^ 1c', W, R, V ) if answer == "Maybe" else announce( '¬<bea> 1a ^ 1b ^ 1c', W, R, V )

	answer = "Yes" if multiagent_solve( '[cal] 1a ^ 1b ^ 1c', W, R, V, w ) else "No"
	print( 'Cal:', answer )



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
