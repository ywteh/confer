import httplib, urllib, json

'''
@author: Anant Bhardwaj
@date: Jan 13, 2014

A sample of how to use confer APIs
'''


def http_post(host, path, params):
	conn = httplib.HTTPConnection(host)
	headers = {
      "Content-type": "application/x-www-form-urlencoded",
			"Accept": "text/plain"
    }
	params = urllib.urlencode(params)
	conn.request("POST", path, params, headers)	
	res = conn.getresponse().read()
	return json.loads(res)

print http_post('confer.csail.mit.edu', '/api/likes', {
    'login_id': 'anantb@csail.mit.edu',
    'conf_id': 'cscw2014', 'application_id':
    'common_ties',
    'application_token': 'xxx'
  })

print http_post('confer.csail.mit.edu', '/api/similar_people', {
    'login_id': 'anantb@csail.mit.edu',
    'conf_id': 'cscw2014', 'application_id':
    'common_ties',
    'application_token': 'xxx'
  })