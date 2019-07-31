import time


class Stopwatch:
	def __init__(self):
		self.start = None
		self.end = None

	def __enter__(self):
		self.start = time.time()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.end = time.time()

	@property
	def result(self):
		return (self.end - self.start)
