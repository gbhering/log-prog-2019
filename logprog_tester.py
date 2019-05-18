from logprog_basic import solve as basic_solve
from logprog_modal import solve as modal_solve
from logprog_multiagent import solve as multiagent_solve
from logprog_announcements import announce, make_euclidean

def test_announcements():
	V = {
		'0a' : [ '00', '01' ],
		'1a' : [ '10', '11' ],
		'0b' : [ '10', '10' ],
		'1b' : [ '01', '11' ]
	}
	W = [ '00', '01', '10', '11' ]
	R = {
		'ana' : { '00': [ '01' ], '01': [ '00' ], '10': [ '11' ], '11': [ '10' ] },
		'bea' : { '00': [ '10' ], '10': [ '00' ], '01': [ '11' ], '11': [ '01' ] },
	}
	w = '11'

	make_euclidean(R)
	print( 'Announcement test: Do you both want coffee?' ) 
	ana_answer = "Maybe" if multiagent_solve( '<ana> 1a ^ 1b', W, R, V, w ) else "No"
	print( 'Ana:', ana_answer )
	W = announce( '<ana> 1a ^ 1b', W, R, V ) if ana_answer == "Maybe" else announce( '¬<ana> 1a ^ 1b', W, R, V )
	print( 'Bea:', "Yes" if multiagent_solve( '[bea] 1a ^ 1b', W, R, V, w ) else "No" )



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
