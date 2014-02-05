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

host = 'confer.csail.mit.edu'
app_id = 'test_app' #  your registered app name
app_token = '68b6fdc3285886ac0f9f3d01bc86a9ad06867777' # your app token
conf_id = 'cscw2014' # conference id

# get likes for a confer login_id
print http_post(host, '/api/likes', {
    'login_id': 'anantb@mit.edu',
    'conf_id': conf_id,
    'app_id': app_id,
    'app_token': app_token
  })

# get similar_people for a confer login_id
print http_post(host, '/api/similar_people', {
    'login_id': 'anantb@mit.edu',
    'conf_id': conf_id,
    'app_id': app_id,
    'app_token': app_token
  })