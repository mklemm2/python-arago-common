from gevent.lock import BoundedSemaphore
from gevent.event import Event

class FlipState(object):
	class EventProxy(object):
		def __init__(self, a, b):
			self._sem = BoundedSemaphore()
			with self._sem:
				self._a = a
				self._b = b

		def set(self):
			with self._sem:
				self._a.set()
				self._b.clear()

		def clear(self):
			with self._sem:
				self._b.set()
				self._a.clear()

		def is_set(self):
			return self._a.is_set()

		def wait(self):
			return self._a.wait()

	def __init__(self, on="on", off="off"):
		self._on_name = on
		self._off_name = off
		self._on = Event()
		self._off = Event()
		setattr(self, self._on_name, FlipState.EventProxy(self._on, self._off))
		setattr(self, self._off_name, FlipState.EventProxy(self._off, self._on))
		getattr(self, self._off_name).set()

	def flip(self):
		if getattr(self, self._on_name).is_set():
			getattr(self, self._on_name).clear()
		else:
			getattr(self, self._on_name).set()
