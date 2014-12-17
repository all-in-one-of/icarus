#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsPreviewLauncher

import os
import gpsPreview__main__
	
#launches GPS Preview UI based on environment
def launch(env=None):
	if not env:
		return
	os.environ['ICARUSENVAWARE'] = env
	reload(gpsPreview__main__)
