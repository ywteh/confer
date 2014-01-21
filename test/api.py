import httplib, urllib, json


def http_post(url, params):
	conn = httplib.HTTPConnection("confer.csail.mit.edu")
	headers = {"Content-type": "application/x-www-form-urlencoded",
			"Accept": "text/plain"}
	params = urllib.urlencode(params)
	conn.request("POST", url, params, headers)	
	res = conn.getresponse().read()
	return json.loads(res)



print http_post('/api/likes', {'login_id': 'anantb@csail.mit.edu', 'conf_id': 'cscw2014', 'application_id': 'common_ties', 'application_token': 'xxx'})
print http_post('/api/similar_people', {'login_id': 'anantb@csail.mit.edu', 'conf_id': 'cscw2014', 'application_id': 'common_ties', 'application_token': 'xxx'})