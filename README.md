## basic_implementation.py
It is in your hands to make sure your formulae are well formed. The program has basic error handling, but it still has ways to go until it is perfect.

### Basic usage
Just use the function `solve(phi, V)`. The output will be `bool`. 

#### Format
Provide a the formula as a `str` making sure no variable names will coincide with operator names. Ensure parens are be balanced, and not empty.
To evaluate the formula, the algorithm needs a `dict` with `bool` values for each literal.

#### Example
```python
V = { 'A': True, 'B': False, 'C': False, 'D': True }

solve("A AND B",V) # True
solve("A OR B",V) # True
solve("NOT A",V) # False
solve("(A OR B) AND (C OR D)",V) # True
solve("(A->B)->(C->D)",V) # True
```

### Operators
Listed in priority order. The parens `(` and `)` can be used to specify order of resolution.
#### Unary operators 
`NOT`
#### Binary operators 
`AND`, `OR` and `->` 


## modal_implementation.py
It is in your hands to make sure your formulae are well formed. The program has basic error handling, but it still has ways to go until it is perfect.
There's no sanity checking on the model whatsoever.

### Basic usage
Just use the function `solve( phi, W, R, V, w )`. The output will be `bool`. 

#### Format
Provide a the formula as a `str` making sure no variable names will coincide with operator names. Ensure parens are be balanced, and not empty.
The model is expressed by:
- A `dict` where each literal is associated to a `list` of states where it is true; 
- a `list` of states and
- another `dict` with `lists` representing each state and the states they connect to.

#### Example
Let us use this example model:

![example graph picture](./test_model.png)

Which can be expressed by this code:
```python
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

solve( "q AND r", W, R, V, "s1" ) # True
solve( "q OR r", W, R, V, "s3" ) # False
solve( "SOME p", W, R, V, "s3" ) # True
solve( "ALL NOT r", W, R, V, "s4" ) # False
```

### Operators
Listed in priority order. The parens `(` and `)` can be used to specify order of resolution.
#### Unary operators 
`NOT`, `SOME` and `ALL`
#### Binary operators 
`AND`, `OR` and `->` 

## Useful links
[List of logic symbols](https://en.wikipedia.org/wiki/List_of_logic_symbols) on Wikipedia

[Modal Logic Playground](https://rkirsling.github.io/modallogic/) by Ross Kirsling ~~who stole the idea of doing it long before I had it~~
