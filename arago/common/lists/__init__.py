import itertools

def merge_lists(*lists):
	return [{"key": key, "value": value} if value else {"value": key}
	        for key, value in {
			        item['key'] if 'key' in item else item['value']:item['value']
			        if 'key' in item else None
			        for item in itertools.chain(*lists)
	        }.items()]
