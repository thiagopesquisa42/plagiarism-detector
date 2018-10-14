#env python3
import subprocess
import os

def callOldProcess(
	pathToOldPythonCore = r"C:\Users\thiagopesquisa42\Anaconda3\envs\py27\python.exe",
	pathToScript = "pythonOldExample.py",
	argumentList = ['Mr', 'Thiago Pesquisa 42']):
	commandLine_PythonOld_Arguments = [pathToOldPythonCore, pathToScript] + argumentList
	process = subprocess.Popen(
		commandLine_PythonOld_Arguments, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE,
		shell = True)
	output, error = process.communicate()
	output_list = output.decode('ascii').splitlines()
	error = error.decode('ascii')
	if((error is not None) and (error is not '') and (not error.isspace())):
		raise ChildProcessError(error)
	return (output_list)