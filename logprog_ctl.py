from collections import defaultdict

class Kripke:
	""" K = < S(tates), R(elationships), L(abels) > """
	def __init__(self, S=[], R=[], L={}):
		self.S = set(S)
		self.R = set(R)
		self.L = defaultdict(list).update(L)

