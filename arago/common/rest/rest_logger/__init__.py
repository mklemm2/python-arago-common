import logging
#from arago.common.helper import prettify
import json

class RESTLogger(object):
	def __init__(self):
		self.logger = logging.getLogger('root')
	def process_request(self, req, resp):
		if 'doc' in req.context:
			self.logger.trace(
				"JSON data received via {op} at {uri}:\n".format(
					op=req.method, uri=req.relative_uri)
				+ json.dumps(req.context['doc'], sort_keys=True, indent=4)
				)

	def process_response(self, req, resp, resource):
		if 'result' in resp.context:
			self.logger.trace(
				"Response status: {stat}, ".format(stat=resp.status)
				+ "JSON data sent:\n"
				+ json.dumps(resp.context['result'], sort_keys=True, indent=4)
				)
