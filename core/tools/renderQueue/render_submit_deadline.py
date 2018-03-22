#!/usr/bin/python

# [Icarus] render_submit_deadline.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2018 Gramercy Park Studios
#
# Batch Render Submitter
# This module contains functions specifically for submitting jobs to Deadline.


import os
import re
import sys
import traceback

# Import custom modules
import osOps
import verbose


def get_pools():
	""" Get Deadline pools and return in a list.
	"""
	try:
		pools = osOps.execute([os.environ['DEADLINECMDVERSION'], '-pools'])[1]
		return pools.splitlines()
	except:
		verbose.warning("Could not retrieve Deadline pools.")
		return None


def get_groups():
	""" Get Deadline groups and return in a list.
	"""
	try:
		groups = osOps.execute([os.environ['DEADLINECMDVERSION'], '-groups'])[1]
		return groups.splitlines()
	except:
		verbose.warning("Could not retrieve Deadline groups.")
		return None


def settings_filename(scene, suffix=""):
	""" Determine the path to the settings file based on the full path of the
		scene file. N.B. This function is duplicated in render_submit.py
	"""
	if os.path.isfile(scene):
		sceneDir, sceneFile = os.path.split(scene)
		settingsDir = os.path.join(sceneDir, os.environ['DATAFILESRELATIVEDIR'])
		settingsFile = osOps.sanitize(sceneFile, replace='_') + suffix

		# Create settings directory if it doesn't exist
		if not os.path.isdir(settingsDir):
			osOps.createDir(settingsDir)

		return os.path.join(settingsDir, settingsFile)

	else:
		return False


def generate_job_info_file(**kwargs):
	""" Generate job submission info file.
	"""
	if kwargs['renderLayer']:
		jobInfoFileSuffix = "_%s_deadlineJobInfo.txt" %kwargs['renderLayer']
	else:
		jobInfoFileSuffix = "_deadlineJobInfo.txt"
	jobInfoFile = settings_filename(kwargs['scene'], suffix=jobInfoFileSuffix)

	fh = open(jobInfoFile, 'w')
	fh.write("Plugin=%s\n" %kwargs['plugin'])
	if kwargs['renderLayer']:
		fh.write("Name=%s - %s\n" %(kwargs['jobName'], kwargs['renderLayer']))
		fh.write("BatchName=%s\n" %kwargs['jobName'])
	else:
		fh.write("Name=%s\n" %kwargs['jobName'])
	fh.write("Comment=%s\n" %kwargs['comment'])
	fh.write("Frames=%s\n" %kwargs['frames'])
	fh.write("ChunkSize=%s\n" %kwargs['taskSize'])
	fh.write("Pool=%s\n" %kwargs['pool'])
	fh.write("Group=%s\n" %kwargs['group'])
	fh.write("Priority=%s\n" %kwargs['priority'])
	fh.write("UserName=%s\n" %kwargs['username'])
	if kwargs['priority'] == 0:
		fh.write("InitialStatus=Suspended\n")
	for i, outputPath in enumerate(kwargs['output']):
		fh.write("OutputDirectory%d=%s\n" %(i, outputPath[0]))
		fh.write("OutputFilename%d=%s\n" %(i, outputPath[1]))
	# fh.write("IncludeEnvironment=True\n")
	# fh.write("EnvironmentKeyValue0=USERNAME=\n")
	# fh.write("EnvironmentKeyValue1=USERPROFILE=\n")
	# fh.write("EnvironmentKeyValue2=LOCALAPPDATA=\n")
	# fh.write("EnvironmentKeyValue3=TEMP=\n")
	# fh.write("EnvironmentKeyValue3=TMP=\n")
	for i, envVar in enumerate(kwargs['envVars']):
		fh.write("EnvironmentKeyValue%d=%s=%s\n" %(i, envVar, os.environ[envVar]))
	fh.write("ExtraInfo0=%s\n" %os.environ['JOB'])
	fh.write("ExtraInfo1=%s\n" %os.environ['SHOT'])
	fh.close()

	return jobInfoFile


def generate_plugin_info_file(**kwargs):
	""" Generate plugin submission info file.
	"""
	if kwargs['renderLayer']:
		pluginInfoFileSuffix = "_%s_deadlinePluginInfo.txt" %kwargs['renderLayer']
	else:
		pluginInfoFileSuffix = "_deadlinePluginInfo.txt"
	pluginInfoFile = settings_filename(kwargs['scene'], suffix=pluginInfoFileSuffix)
	fh = open(pluginInfoFile, 'w')

	# Command Line -----------------------------------------------------------
	if kwargs['plugin'] == "CommandLine":
		pass
		# fh.write("Executable=%s\n" %kwargs['executable'])
		# fh.write("Arguments=%s\n" %kwargs['flags'])
		# fh.write("Shell=Default\n")
		# fh.write("ShellExecute=False\n")
		# fh.write("StartupDirectory=%s\n" %kwargs['startupDir'])

	# Maya -------------------------------------------------------------------
	elif kwargs['plugin'] == "MayaBatch":
		fh.write("Version=%s\n" %kwargs['version'])
		fh.write("Build=64bit\n")
		fh.write("Renderer=%s\n" %kwargs['renderer'])
		fh.write("StrictErrorChecking=1\n")
		fh.write("ProjectPath=%s\n" %kwargs['mayaProject'])
		fh.write("OutputFilePath=%s\n" %kwargs['outputFilePath'])
		fh.write("OutputFilePrefix=%s\n" %kwargs['outputFilePrefix'])
		fh.write("SceneFile=%s\n" %kwargs['scene'])
		if kwargs['renderLayer']:
			fh.write("UsingRenderLayers=1\n")
			fh.write("UseLegacyRenderLayers=1\n")
			fh.write("RenderLayer=%s\n" %kwargs['renderLayer'])

	# Nuke -------------------------------------------------------------------
	elif kwargs['plugin'] == "Nuke":
		fh.write("BatchMode=True\n")
		# fh.write("BatchModeIsMovie=%s\n" %kwargs['isMovie'])
		fh.write("NukeX=%s\n" %kwargs['nukeX'])
		fh.write("Version=%s\n" %kwargs['version'])
		fh.write("SceneFile=%s\n" %kwargs['scene'])
		if kwargs['renderLayers']:
			fh.write("WriteNode=%s\n" %kwargs['renderLayer'])
			fh.write("BatchModeIsMovie=%s\n" %kwargs['isMovie'])

	fh.close()

	return pluginInfoFile


def generate_batch_file(scene, jobInfoFileList, pluginInfoFileList):
	""" Generate batch job submission file given corresponding lists of job
		and plugin info files.
	"""
	batchSubmissionFile = settings_filename(scene, suffix="_deadlineBatchArgs.txt")
	fh = open(batchSubmissionFile, 'w')
	fh.write("-SubmitMultipleJobs\n")
	for i in range(len(jobInfoFileList)):
		fh.write("-job\n")
		fh.write("%s\n" %jobInfoFileList[i])
		fh.write("%s\n" %pluginInfoFileList[i])
	fh.close()

	return batchSubmissionFile


def submit_job(**kwargs):
	""" Submit job to Deadline.
	"""
	cmd_output = ""
	result_msg = ""

	if kwargs is not None:
		for key, value in kwargs.items(): # iteritems(): for Python 2.x
			verbose.print_("%24s = %s" %(key, value))

	try:
		if kwargs['renderLayers']:  # Batch submission -----------------------
			# Generate submission info files
			num_jobs = 0
			jobInfoFileList = []
			pluginInfoFileList = []
			#for renderLayer in kwargs['renderLayers'].split(", "):
			for renderLayer in re.split(r',\s*', kwargs['renderLayers']): # use re for more versatility, or even better pass as list
				kwargs['renderLayer'] = renderLayer
				# kwargs['isMovie'] = False
				jobInfoFile = generate_job_info_file(**kwargs)
				jobInfoFileList.append(jobInfoFile)
				pluginInfoFile = generate_plugin_info_file(**kwargs)
				pluginInfoFileList.append(pluginInfoFile)
				num_jobs += 1

			# Generate batch file
			batchSubmissionFile = generate_batch_file(
				kwargs['scene'], 
				jobInfoFileList, 
				pluginInfoFileList)

			# Execute deadlinecommand
			cmd_result, cmd_output = osOps.execute([os.environ['DEADLINECMDVERSION'], batchSubmissionFile])
			if cmd_result:
				result_msg = "Successfully submitted %d %s to Deadline." %(num_jobs, verbose.pluralise("job", num_jobs))

			# Delete submission info files
			if int(os.environ['IC_VERBOSITY']) < 4:
				for jobInfoFile in jobInfoFileList:
					osOps.recurseRemove(jobInfoFile)
				for pluginInfoFile in pluginInfoFileList:
					osOps.recurseRemove(pluginInfoFile)
				osOps.recurseRemove(batchSubmissionFile)

		else:  # Single job submission ---------------------------------------
			# Generate submission info files
			kwargs['renderLayer'] = None
			jobInfoFile = generate_job_info_file(**kwargs)
			pluginInfoFile = generate_plugin_info_file(**kwargs)

			# Execute deadlinecommand
			cmd_result, cmd_output = osOps.execute([os.environ['DEADLINECMDVERSION'], jobInfoFile, pluginInfoFile])
			if cmd_result:
				result_msg = "Successfully submitted job to Deadline."

			# Delete submission info files
			if int(os.environ['IC_VERBOSITY']) < 4:
				osOps.recurseRemove(jobInfoFile)
				osOps.recurseRemove(pluginInfoFile)

		if cmd_result:
			result = True
			print(cmd_output) #.decode())
			verbose.message(result_msg)
		else:
			raise RuntimeError(cmd_output)

	except:  # Submission failed ---------------------------------------------
		result = False
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		result_msg = "Failed to submit job to Deadline."
		verbose.error(result_msg)
		if (exc_type == RuntimeError) and cmd_output:
			result_msg += "\n" + cmd_output
		else:
			result_msg += "\nCheck console output for details."
		#output_str = "Either the Deadline executable could not be found, or the submission info files could not be written."
		#output_str = traceback.format_exception_only(exc_type, exc_value)[0]

	return result, result_msg
