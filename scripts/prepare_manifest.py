import sys, os, json, csv, re, difflib

static_manifest='''CACHE MANIFEST
# version 1.0002

/home
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
home_manifest = ''

post_manifest = '''

NETWORK:
*
'''

for conf in os.listdir("server/static/conf/"):
	if '.' in conf:
		continue

	dynamic_manifest = ''
	dynamic_path = '/static/conf/%s/' %(conf)

	dynamic_manifest += dynamic_path + 'data/papers.json\n'
	dynamic_manifest += dynamic_path + 'data/sessions.json\n'
	dynamic_manifest += dynamic_path + 'data/offline_recs.json\n'
	dynamic_manifest += dynamic_path + 'data/schedule.json\n'
	dynamic_manifest += dynamic_path + 'data/filters.json\n'
	dynamic_manifest += dynamic_path + 'logo/logo.png\n'

	home_manifest += dynamic_path + 'logo/cover.png\n'

	p = open('server/static/conf/%s/cache.manifest' %(conf),'w+')
	p.write(static_manifest + dynamic_manifest + post_manifest)

p = open('server/static/conf/cache.manifest','w+')
p.write(static_manifest + home_manifest + post_manifest)
 