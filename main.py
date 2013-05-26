"""
	Version:	0.1 - Beta
	Author:		Memleak13
	Date:		25.05.13

	This is the main module which is initilized by Apache.
	Permissions must be set correctly, all files will be created with 
	www-data permissions, directories need to writable by www-data
	
	Apache -> main.py -> index.html -> main.py -> dscript.py
"""
import web
import sys
import os
import json

#Set absolute path for apache
root = os.path.dirname(__file__)
render = web.template.render(os.path.join(root, 'templates'), cache=False)

urls = (
	'/', 'index',
	'/runscript', 'runscript',
	'/counter', 'counter'
)
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc() #when using mod_wsgi

class index:
	"""The initial site allows the user to select the macdomain."""
	
	def GET(self):
		"""Returns /templates/index.html"""
		return render.index()
		
class runscript:
	"""Runs dscript.py"""
	
	def GET(self):
		"""Checks conditions before running script
		
		Checks if status file exists and if the script is already running.
		"""
		getInput = web.input(macdomain=None)
		try:
			fh_status = open('/var/www/dscript/static/status')
			data = json.loads(fh_status.read())
			if data['RUN_STATE'] is 1:
				return (1)
			else:
				os.system('/var/www/dscript/dscript.py %s &' 
						  % getInput.macdomain)
		#Throw exception if file does not exist and runs dscript.py. dscript
		#creates the file.
		except:
			os.system('/var/www/dscript/dscript.py %s &' % getInput.macdomain)

class counter:
	"""Returns run state and counter"""
	
	def GET(self):
		fh_status = open('/var/www/dscript/static/status')
		data = json.loads(fh_status.read())
		fh_status.close()
		web.header('Content-Type', 'application/json')
		return json.dumps(data)