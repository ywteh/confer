from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','server.views.home'),
	url(r'^home$', 'server.views.home'),
    url(r'^team', 'server.views.team'),
	
	url(r'^data', 'server.views.data'),
    url(r'^recs', 'server.views.get_recs'),
    url(r'^like/(\w+)$', 'server.views.like'),
    url(r'^log/(\w+)$', 'server.views.log'),

    url(r'^login', 'server.auth.login'),
    url(r'^register', 'server.auth.register'),
    url(r'^logout', 'server.auth.logout'),

    url(r'^forgot', 'server.auth.forgot'),
    url(r'^reset/(\w+)', 'server.auth.reset'),
    url(r'^settings', 'server.auth.settings'),

    #move this matching in the end
    url(r'^(\w+?)/papers$', 'server.views.papers'),
    url(r'^(\w+?)/schedule$', 'server.views.schedule'),
    url(r'^(\w+?)/paper', 'server.views.paper'),
    url(r'^(\w+?)/meetups', 'server.views.meetups'),
    url(r'^(\w+)$', 'server.views.conf'),
    url(r'^(\w+?)/$', 'server.views.conf'),
)