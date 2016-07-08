#!/usr/bin/python

# [GPS] menu.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Customises Nuke's menus and toolbars.


#third party gizmos and plugins menu build
import pixelfudger
#
import gpsSave


# Detect if running app is Nuke or NukeX
if nuke.env['nukex']:
	nukeType = 'NukeX'
else:
	nukeType = 'Nuke'


# Command strings
readNode = 'import gpsNodes; gpsNodes.read_create()'
writeNode = 'import gpsNodes; gpsNodes.write_create()'
save = 'import gpsSave; gpsSave.save(incr=False)'
saveAs = 'import gpsSave; gpsSave.save(saveAs=True)'
incrSave = 'import gpsSave; gpsSave.save(incr=True)'
openScript = 'nuke.scriptOpen(\"%s/.\")' % os.environ["NUKESCRIPTSDIR"].replace('\\', '/')
openScriptsDir = 'import openDirs; openDirs.openNukeScripts()'
openRendersDir = 'import openDirs; openDirs.openNukeRenders()'
openElementsDir = 'import openDirs; openDirs.openNukeElements()'
openShotDir = 'import openDirs; openDirs.openShot()'
openJobDir = 'import openDirs; openDirs.openJob()'
openElementsLibDir = 'import openDirs; openDirs.openElementsLib()'
launchProdBoard  = 'import launchApps; launchApps.prodBoard()'
launchNuke = 'import launchApps; launchApps.launch("%s")' % nukeType
launchIcarus = 'reload(icarus__main__)'
launchDjv = 'import launchApps; launchApps.djv()'
launchHieroPlayer = 'import launchApps; launchApps.launch("HieroPlayer")'
versionUp = 'import switchVersion; switchVersion.versionUp()'
versionDown = 'import switchVersion; switchVersion.versionDown()'
versionLatest = 'import switchVersion; switchVersion.versionLatest()'
submitRender = 'import nukeOps; nukeOps.submitRender()'
submitRenderSelected = 'import nukeOps; nukeOps.submitRenderSelected()'


#NUKE MENU
nukeMenu = nuke.menu('Nuke')
gpsMenu = nukeMenu.addMenu('GPS', index=6)


#NODES MENU
nodesMenu = nuke.menu('Nodes')


#GPS NODES MENU
#gps
gpsMenu_nodes = nodesMenu.addMenu('GPS', icon='gps.png')
deflickerVelocity_cmd = gpsMenu_nodes.addCommand('Deflicker Velocity', "nuke.createNode('deflickerVelocity')", icon='newScript.png')
#separator
nodesMenu.addSeparator()
#new
newMenu_nodes = nodesMenu.addCommand('New', launchNuke, '^n', icon='newScript.png')
#open
openMenu_nodes = nodesMenu.addMenu('Open', icon='openScript.png')
openMenu_nodes.addCommand('Open...', openScript, '^o', icon='openScript.png')
openRecentMenu_nodes = openMenu_nodes.addMenu('Open Recent', icon='openScript.png')
#save
incrementalSaveMenu_nodes =  nodesMenu.addCommand('Incremental Save', incrSave, 'alt+shift+s', icon='incrementalSave.png')
saveMenu_nodes =  nodesMenu.addCommand('Save', save, '^s', icon='saveScript.png')
#switch version
switchVersionMenu = nodesMenu.addMenu('Switch Version', icon='switchVersion.png')
versionLatestMenu_nodes = switchVersionMenu.addCommand('Version to Latest', versionLatest, 'alt+shift+up', icon='versionLatest.png')
versionUpMenu_nodes = switchVersionMenu.addCommand('Version Up', versionUp, 'alt+up', icon='versionUp.png')
versionDownMenu_nodes = switchVersionMenu.addCommand('Version Down', versionDown, 'alt+down', icon='versionDown.png')
#submit render
submitRenderMenu = nodesMenu.addMenu('Submit to Render Queue', icon='gpsSubmitRender.png')
submitRenderMenu_nodes = submitRenderMenu.addCommand('Submit render job', submitRender, icon='gpsSubmitRender.png')
submitRenderSelectedMenu_nodes = submitRenderMenu.addCommand('Submit render job (selected write node only)', submitRenderSelected, icon='gpsSubmitRender.png')
#icarusUI
icarusMenu_nodes = nodesMenu.addCommand('Icarus UI', launchIcarus, icon='icarus.png')
#production board
productionBoardMenu_nodes = nodesMenu.addCommand('Production Board', launchProdBoard, icon='productionBoard.png')
#djv
reviewMenu = nodesMenu.addMenu('Review', icon='review.png')
hieroPlayerMenu_nodes = reviewMenu.addCommand('HieroPlayer', launchHieroPlayer, icon='hieroPlayer.png')
djvMenu_nodes = reviewMenu.addCommand('djv_view', launchDjv, icon='djv.png')
#browse
browseMenu_nodes = nodesMenu.addMenu('Browse', icon='browse.png')
browseMenu_nodes.addCommand('Browse Scripts', openScriptsDir)
browseMenu_nodes.addCommand('Browse Renders', openRendersDir)
browseMenu_nodes.addCommand('Browse Elements', openElementsDir)
browseMenu_nodes.addCommand('Browse Shot', openShotDir)
browseMenu_nodes.addCommand('Browse Job', openJobDir)
browseMenu_nodes.addCommand('Browse Elements Library', openElementsLibDir)


#GPS MENU
#switch version
switchVersionMenu_gps = gpsMenu.addMenu('Switch Version', icon='switchVersion.png')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('Version to Latest', versionLatest, icon='versionLatest.png')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('Version Up', versionUp, icon='versionUp.png')
versionUpMenu_gps = switchVersionMenu_gps.addCommand('Version Down', versionDown, icon='versionDown.png')
#separator
gpsMenu.addSeparator()
#icarusUI
icarusMenu_gps = gpsMenu.addCommand('Icarus UI...', launchIcarus, icon='icarus.png')
#separator
gpsMenu.addSeparator()
#production board
productionBoardMenu_gps = gpsMenu.addCommand('Production Board', launchProdBoard, icon='productionBoard.png')
#separator
gpsMenu.addSeparator()
#browse
browseMenu_gps = gpsMenu.addMenu('Browse', icon='browse.png')
browseMenu_gps.addCommand('Browse Scripts', openScriptsDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Renders', openRendersDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Elements', openElementsDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Shot', openShotDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Job', openJobDir, icon='browse.png')
browseMenu_gps.addCommand('Browse Elements Library', openElementsLibDir, icon='browse.png')


#IMAGE MENU
imageMenu = nodesMenu.menu('Image')
imageMenu.addCommand('[GPS] Read', readNode, icon='newScript.png', index=0)
#imageMenu.addCommand('[GPS] Read', readNode, 'r', icon='newScript.png', index=0)
#imageMenu.addCommand('[GPS] Write', writeNode, icon='newScript.png', index=1)
imageMenu.addCommand('[GPS] Write', writeNode, 'w', icon='newScript.png', index=1)


#RENDER MENU
imageMenu = nukeMenu.menu('Render')
imageMenu.addCommand('[GPS] Submit render job...', submitRender, icon='gpsSubmitRender.png', index=4)
imageMenu.addCommand('[GPS] Submit render job (selected write node only)...', submitRenderSelected, icon='gpsSubmitRender.png', index=5)


#FILE MENU
fileMenu = nukeMenu.menu('File')
#new
newMenu_gps = fileMenu.addCommand('[GPS] New', launchNuke, '^n', icon='newScript.png', index=0)
#open
openMenu_gps = fileMenu.addCommand('[GPS] Open...', openScript, '^o', icon='openScript.png', index=1)
#open recent
openRecentMenu_gps = fileMenu.addMenu('[GPS] Open Recent', icon='openScript.png', index=2)
#separator
fileMenu.addSeparator(index=3)
#save
saveMenu_gps =  fileMenu.addCommand('[GPS] Save', save, '^s', icon='saveScript.png', index=4)
#save as
saveAsMenu_gps =  fileMenu.addCommand('[GPS] Save As...', saveAs, '^shift+s', icon='saveScript.png', index=5)
#incremental save
saveIncrementalMenu_gps =  fileMenu.addCommand('[GPS] Incremental Save', incrSave, 'alt+shift+s', icon='incrementalSave.png', index=6)
#separator
fileMenu.addSeparator(index=7)


# Remove default file menu items...

# Nuke 8.x
fileMenu = nukeMenu.findItem('File')
fileMenu.removeItem('New')
fileMenu.removeItem('Open...')
fileMenu.removeItem('Save')
fileMenu.removeItem('Save As...')
fileMenu.removeItem('Save New Version')
fileMenu.removeItem('Recent Files')

# Nuke 9.x
fileMenu.removeItem('New Comp...')
fileMenu.removeItem('Open Comp...')
fileMenu.removeItem('Open Recent Comp')
fileMenu.removeItem('Close Comp')
fileMenu.removeItem('Save Comp')
fileMenu.removeItem('Save Comp As...')
fileMenu.removeItem('Save New Comp Version')


# Initialise recent files menu...
gpsSave.updateRecentFilesMenu(openRecentMenu_gps)
gpsSave.updateRecentFilesMenu(openRecentMenu_nodes)


# Add callback function to add script to recent files on script load...
nuke.addOnScriptLoad( gpsSave.updateRecentFiles )
