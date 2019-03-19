## basic_implementation.py
Observe there is no error handling whatsoever, the user is entirely responsible for providing
 a well formed/formatted formula.

### Format
Provide a `str()` with one space between each literal and operator,
 and a `dict()` with `bool()` values for each literal.
Parens should be balanced, and not empty.

##### Examples
```python
v = {
	'A':True,
	'B':False,
	'C':True,
	'D':False
}

solve("A AND B",v)
solve("A OR B",v)
solve("NOT A",v)
solve("(A OR B) AND (C OR D)",v)
```

### Operators
`OR`, `AND`, and `NOT`


# Useful links
[Wikipedia's list of logic symbols](https://en.wikipedia.org/wiki/List_of_logic_symbols)
