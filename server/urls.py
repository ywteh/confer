#from django.conf.urls import patterns, include, url
from django.conf.urls import include, url

from server import views as server_views
from server import auth as server_auth

urlpatterns = [ #patterns('',
    url(r'^$',server_views.home, name='home'),
    url(r'^home$', server_views.home, name="home"),
    url(r'^team', server_views.team, name="team"),
    url(r'^credits', server_views.credits, name="credits"),
    
    url(r'^data', server_views.data, name="data"),
    
    url(r'^like/(\w+)$', server_views.like, name="like"),
    url(r'^person_like/(\w+)$', server_views.person_like, name="person_like"),
    url(r'^log/(\w+)$', server_views.log, name="log"),

    url(r'^login', server_auth.login, name="login"),
    url(r'^register', server_auth.register, name="register"),
    url(r'^logout', server_auth.logout, name="logout"),

    url(r'^forgot', server_auth.forgot, name="forgot"),
    url(r'^reset/(\w+)', server_auth.reset, name="reset"),
    url(r'^verify/(\w+)', server_auth.verify, name="verify"),

    #confer apps APIs
    url(r'^api/likes$', server_views.likes, name="likes"),
    url(r'^api/similar_people$', server_views.similar_people, name="similar_people"),

    #confer developer APIs
    url(r'^developer$', server_views.developer, name="developer"),
    url(r'^developer/apps$', server_views.apps, name="apps"),
    url(r'^developer/register_app$', server_views.register_app, name="register_app"),
    url(r'^developer/allow_access$', server_views.allow_access, name="allow_access"),

    #confer settings
    url(r'^(\w+?)/settings', server_views.settings, name="settings"),

    #move this matching in the end
    url(r'^(\w+?)/visualizations$', server_views.visualizations, name="visualizations"),
    url(r'^(\w+?)/feed$', server_views.feed, name="feed"),
    url(r'^(\w+?)/network_graph$', server_views.network_graph, name="network_graph"),
    
    url(r'^(\w+?)/papers$', server_views.papers, name="papers"),
    url(r'^(\w+?)/schedule$', server_views.schedule, name="schedule"),
    url(r'^(\w+?)/paper', server_views.paper, name="paper"),
    url(r'^(\w+?)/meetups', server_views.meetups, name="meetups"),
    url(r'^(\w+?)/admin$', server_views.admin, name="admin"),
    url(r'^(\w+?)/update_conference$', server_views.update_conference, name="update_conference"),
    url(r'^(\w+)$', server_views.conf, name="conf"),
    url(r'^(\w+?)/$', server_views.conf, name="conf"),
    url(r'^(\w+?)/anonymized_data_dump$', server_views.anonymized_data_dump, name="anonymized_data_dump"),
    url(r'^(\w+?)/all_data_dump$', server_views.all_data_dump, name="all_data_dump"),
    
    #url(r'^recs', server_views.get_recs, name="get_recs"),
]
