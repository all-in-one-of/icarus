#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:setPermissions
#copyright	:Gramercy Park Studios


#sets user permissions in publish directories
import os, time

def set_(pblTo):
	#allows two seconds of sleeping time to allow the server to update
	time.sleep(2)
	try:
		os.system('chmod -R 777 %s' % pblTo)
	except:
		return
	return 1
