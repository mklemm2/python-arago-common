import gevent


def backoff(retries=10, base=0.01, cap=5):
	for a in range(retries):
		yield a
		gevent.sleep(min(cap, base * 2 ** a))
