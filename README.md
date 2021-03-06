## log-prog-2019
This is a series of python scripts that implement a few logic formula verifiers. At the moment, these are: [simple propositional logic](#logprog_basic), [modal logic](#logprog_modal), and [multi-agent modal logic](#logprog_multiagent) (which has a [public announcement extension](#logprog_announcements)).

#### General Guidelines
Run with python3! It is in your hands to make sure your formulae are well formed. The program has basic error handling, but it still has ways to go until it is perfect. Make sure parenthesis are balanced and not empty, and there is no overlap between variable names and operator tokens. There's no sanity checking on the models whatsoever.

Each implementation has a `solve()` method, that takes the formula (`phi`) for verification and data structures that represent the related models. Find below short descriptions, operator lists and examples (refer to [logprog_tester.py](logprog_tester.py) for more).

A few different tokens are used for each operators, you can use them interchangeably and mix and match.

### logprog_basic
Basic propositional logic, exposed here mostly for educational purposes. `solve( phi: str, V: dict ) -> bool` takes a dictionary of literals and uses it to verify the formula.

#### Example
```python
V = { 'A': True, 'B': False, 'C': False, 'D': True }

solve("A AND B",V) # True
solve("A OR B",V) # True
solve("NOT A",V) # False
solve("(A OR B) AND (C OR D)",V) # True
solve("(A->B)->(C->D)",V) # True
```

#### Unary operators 
[ `NOT` | `!` | `¬` ]
#### Binary operators 
[ `AND` | `&` | `∧` ], [ `OR` | `|` | `∨` ], and [ `IMPLIES` | `->` | `→` ]

## modal_implementation
Modal logic uses state models. Verification of forumulae happens in specific states. There are operators that verify whether all or any neighboring states evaluate the formula that follows as true. As this model often represents a belief system, those operators are here called 'necessarily' and 'possibly' respectively.

In this implementation the state model is represented by: 
- a list of states `W`; 
- a dictionary associating each state to a list of other states they are connected to `R` and 
- A dictionary associating literals to lists of states where they are true `V`

So the verifying function is `solve( phi: str, W: list, R: dict, V: dict, w: str ) -> bool`, where `phi` is the formula and `w` the state where it is evaluated. 

#### Example
Let us use this example model:

![example graph picture](./test_model.png)

Which can be expressed by this code:
```python
W = [ 's1', 's2', 's3', 's4', 's5'  ]
R = { 
	's1' : [ 's2', 's3' ], 
	's2' : [ 's5', 's4' ], 
	's3' : [ 's3', 's4' ], 
	's4' : [ 's1', 's5' ], 
	's5' : [ 's5' ] 
}
V = { 
	'p': [ 's3', 's4', 's5' ], 
	'q': [ 's1', 's5' ], 
	'r': [ 's1' ] 
}

solve( "q AND r", W, R, V, "s1" ) # True
solve( "q OR r", W, R, V, "s3" ) # False
solve( "POSSIBLY p", W, R, V, "s3" ) # True
solve( "NECESSARILY NOT r", W, R, V, "s4" ) # False
```

#### Unary operators 
[ `NOT` | `!` | `¬` ], [ `POSSIBLY` | `<>` | `◇` ], and [ `NECESSARILY` | `[]` | `□` ]
#### Binary operators 
[ `AND` | `&` | `∧` ], [ `OR` | `|` | `∨` ], and [ `IMPLIES` | `->` | `→` ]

### logprog_multiagent
This system is an extension of modal logic. In this, again, we take a formula and verify it on a model, but this time there are multiple agents. Each is represented in the graph by different sets of edges, as each sees different relationships between states.

The verifying function takes the same form as in modal logic: `solve( phi: str, W: list, R: dict, V: dict, w: str ) -> bool`, but the dictionaries that contain the edges are nested into another dictionary with each agent as key. 

One possible interpretation of the model is:
- `phi` the question being asked,
- `W` lists the possible worlds, 
- `V` maps which variables are true in each world, 
- `R` contains, for each agent, edges between worlds they cannot distinguish with the variables they know, and
- `w` the real world.

#### Example
Suppose you have two friends going out to have a coffee shop: Ana and Bea. In spite of their choice of venue, they do not know the other's choice of drink. We know that indeed yes, they both want coffee, but we might model the situation as such:

```python
W = [ 'both_want_coffee', 'only_ana_wants_coffee', 'only_bea_wants_coffee', 'neither_want_coffee' ]
V = { 	
	'ana_wants_coffee' : [ 'both_want_coffee', 'only_ana_wants_coffee' ], 
	'ana_wants_tea'    : [ 'neither_want_coffee', 'only_bea_wants_coffee' ], 
	'bea_wants_coffee' : [ 'both_want_coffee', 'only_bea_wants_coffee' ], 
	'bea_wants_tea'    : [ 'neither_want_coffee', 'only_ana_wants_coffee' ]
    }
R = { 	
	'ana' : { 'both_want_coffee'      : [ 'both_want_coffee', 'only_ana_wants_coffee' ], 
		  'neither_want_coffee'   : [ 'neither_want_coffee', 'only_bea_wants_coffee' ],
		  'only_ana_wants_coffee' : [ 'only_ana_wants_coffee', 'both_want_coffee' ],
		  'only_bea_wants_coffee' : [ 'only_bea_wants_coffee', 'neither_want_coffee' ] },
	'bea' : { 'both_want_coffee'      : [ 'both_want_coffee', 'only_bea_wants_coffee' ], 
		  'neither_want_coffee'   : [ 'neither_want_coffee', 'only_ana_wants_coffee' ],
		  'only_ana_wants_coffee' : [ 'only_ana_wants_coffee', 'neither_want_coffee' ],
		  'only_bea_wants_coffee' : [ 'only_bea_wants_coffee', 'both_want_coffee' ] }
     }
w = 'both_want_coffee'
```

We could then ask:

```python
# Does Ana believe both herself and Bea want coffee?
solve( "<ana> ana_wants_coffee AND bea_wants_coffee", W, R, V, w ) # True, she believes it is possible
# Does Bea know Bea wants coffee?
solve( "[bea] bea_wants_coffee", W, R, V, w ) # True, as a matter of fact, she does
# Does both of them know they both want coffee? 
# The two following lines are identical, since Ana and Bea are all the agents
solve( "[ana,bea] ana_wants_coffee AND bea_wants_coffee", W, R, V, w ) # False
solve( "[*] ana_wants_coffee AND bea_wants_coffee", W, R, V, w ) # False
```

#### Unary operators 
[ `NOT` | `!` | `¬` ], `<*>`,`<agent1,agent2,agent3,...>`, `[*]`, and `[agent1,agent2,agent3,...]`
#### Binary operators 
[ `AND` | `&` | `∧` ], [ `OR` | `|` | `∨` ], and [ `IMPLIES` | `->` | `→` ]


### logprog_announcements
This an extension component for multiple agent modal logic. It allows for public announcements to be made, which are simply formulas that are valid in all states or worlds. Its function `announce( phi: str, W: list, R: dict, V: dict )` updates the `W` the list of worlds accordingly.

#### Example
Building upon the prior example:

```python
# Does Ana of them know they both want coffee? 
solve( "[ana] ana_wants_coffee AND bea_wants_coffee", W, R, V, w ) # False, she doesn't
# Bea announces she knows she wants coffee
announce( "[bea] bea_wants_coffee", W, R, V )
# The worlds where Bea knows she does not want coffee are pruned, should we ask Ana again...
solve( "[ana] ana_wants_coffee AND bea_wants_coffee", W, R, V, w ) # True, now she does
```


## Useful links
[List of logic symbols](https://en.wikipedia.org/wiki/List_of_logic_symbols) on Wikipedia

[Modal Logic Playground](https://rkirsling.github.io/modallogic/) by Ross Kirsling ~~who stole the idea of doing it long before I had it~~

[TuLiP](https://github.com/tulip-control/tulip-control) a toolbox of ODBB model manipulation
