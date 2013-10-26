import sys, os, json, csv, re, difflib

static_cache_manifest='''CACHE MANIFEST
# version 1.0002

/team

/static/css/confer.css
/static/css/third-party/jquery-ui.css

/static/javascript/confer.js
/static/javascript/third-party/jquery.min.js
/static/javascript/third-party/jquery-ui.js

/static/fonts/cantoraone.woff

/static/img/affiliation.svg
/static/img/acm.png
/static/img/arrows.ai
/static/img/arts.acorn
/static/img/arts.png
/static/img/authors.svg
/static/img/best-paper.png
/static/img/best.png
/static/img/best.svg
/static/img/calendar.svg
/static/img/cci.acorn
/static/img/cci.png
/static/img/design.acorn
/static/img/design.png
/static/img/down.png
/static/img/engineering.acorn
/static/img/engineering.png
/static/img/games.acorn
/static/img/games.png
/static/img/hci4d.acorn
/static/img/hci4d.png
/static/img/health.acorn
/static/img/health.png
/static/img/management.acorn
/static/img/management.png
/static/img/nominee.png
/static/img/nominee.svg
/static/img/paper.svg
/static/img/right.png
/static/img/sponsors.svg
/static/img/star_closed.svg
/static/img/star_open.png
/static/img/star_open.svg
/static/img/star_yellow.png
/static/img/star_yellow.svg
/static/img/sustainability.acorn
/static/img/sustainability.png
/static/img/user_experience.acorn
/static/img/user_experience.png
/static/img/w_em2.png
/static/img/w_tw.png
/static/img/play.png

'''
home_cache_manifest = ''

static_network_manifest = '''

NETWORK:

'''

for conf in os.listdir("server/static/conf/"):
	if '.' in conf:
		continue

	conf_cache_manifest = ''
	conf_network_manifest = ''
	dynamic_path = '/static/conf/%s/' %(conf)

	conf_cache_manifest += dynamic_path + 'data/papers.json\n'
	conf_cache_manifest += dynamic_path + 'data/sessions.json\n'
	conf_cache_manifest += dynamic_path + 'data/offline_recs.json\n'
	conf_cache_manifest += dynamic_path + 'data/schedule.json\n'
	conf_cache_manifest += dynamic_path + 'data/filters.json\n'
	conf_cache_manifest += dynamic_path + 'logo/logo.png\n'

	conf_network_manifest += dynamic_path + '\n'
	conf_network_manifest += dynamic_path + 'papers\n'
	conf_network_manifest += dynamic_path + 'schedule\n'
	conf_network_manifest += dynamic_path + 'meetups\n'
	conf_network_manifest += dynamic_path + 'paper\n'
	conf_network_manifest += '*\n'

	home_cache_manifest += dynamic_path + 'logo/cover.png\n'

	p = open('server/static/conf/%s/cache.manifest' %(conf),'w+')
	p.write(static_cache_manifest + conf_cache_manifest + conf_network_manifest)

home_network_manifest = static_network_manifest + '*\n'
p = open('server/static/conf/cache.manifest','w+')
p.write(static_cache_manifest + home_cache_manifest + home_network_manifest)
 