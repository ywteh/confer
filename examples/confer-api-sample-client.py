import httplib, urllib, json

'''
@author: Anant Bhardwaj
@date: Jan 13, 2014

A sample of how to use confer APIs
'''

# Step 1: Create your app at http://confer.csail.mit.edu/developer/apps (click on the button 'Create a New App')

# Step 2: You can get your app_token at http://confer.csail.mit.edu/developer/apps at any time

# Step 3: Redirect your first-time users to http://confer.csail.mit.edu/developer/allow_access?app_id=<your app id> 
#         so that they can allow your app to access their data.



host = 'confer.csail.mit.edu'
app_id = 'test_app' #  your app_id
app_token = '68b6fdc3285886ac0f9f3d01bc86a9ad06867777' # your app token
conf_id = 'cscw2014' # conference id


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

# get likes for a confer login_id
print http_post(host, '/api/likes', {
    'login_id': 'anantb@csail.mit.edu',
    'conf_id': conf_id,
    'app_id': app_id,
    'app_token': app_token
  })

# If you get msg = "ACCESS_DENIED" in the response, it means user has revoked the access to your app. 
# You can redirect the user to http://confer.csail.mit.edu/developer/allow_access?app_id=test_app to
# grant the access

# get similar_people for a confer login_id
print http_post(host, '/api/similar_people', {
    'login_id': 'anantb@csail.mit.edu',
    'conf_id': conf_id,
    'app_id': app_id,
    'app_token': app_token
  })

