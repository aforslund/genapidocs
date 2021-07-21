import re
import json
import sys
import os
import argparse

def println(file, string):
	file.write(string+"\n")
			
def resetFileParseState():
	global restApi
	global basePath
	global apiPrefix
	
	restApi = False
	basePath = ""
	apiPrefix = ""
	
def resetMethodParseState():
	global getMethod
	global postMethod
	global requiresLogin
	global multiLineParam
	global parameters
	global returnType

	getMethod = False
	postMethod = False
	requiresLogin = False
	multiLineParam = False
	parameters = ""
	returnType = ""

def printApiDefinition(parameters, returnType):
	global numApisFound
	global oFile
	
	if getMethod:
		oFile.write("HTTP GET ") 
		#, end = '')
	if postMethod:
		oFile.write("HTTP POST ") 
		#, end = '')
	
	println(oFile,apiPrefix+apiPath)

	if requiresLogin:
		println(oFile,"    *** Authorization Required ***")
	println(oFile, "    Parameters: "+parameters)
	println(oFile, "    Returns: "+returnType)
	println(oFile, "")
	
	numApisFound = numApisFound+1
					

arguments = len(sys.argv) - 1

if arguments!=2:
	print("%%%% Usage: GenerateAPIDocsForSpringBoot.py <directory> <outputfile>")
	os._exit(1)
	
mainDir = sys.argv[1]
outputFile = sys.argv[2]

print("** Generating API Docs **")
print()

print("* Reading files from '"+mainDir+"'")
print("* Outputting to '"+outputFile+"'")
print()

javaFiles = [ f for f in os.listdir(mainDir) if os.path.isfile(os.path.join(mainDir,f)) ]

oFile = open(outputFile, "w+")

numApisFound = 0

for javaFile in javaFiles:
	print("* Processing: "+javaFile)
	
	resetFileParseState()
	resetMethodParseState()
	
	file = open(javaFile)
	
	lines = file.readlines()
	
	for line in lines:
		if "@RestController" in line:
			restApi = True
		
		if restApi:	
			if "@RequestMapping" in line:
				apiPrefix = re.search('.*"(.*)".*',line).group(1)
			
			if "@GetMapping" in line:
				if "path" in line:
					apiPath = re.search('.*\{"(.*)"\}.*',line).group(1)
				else:
					apiPath = re.search('.*"(.*)".*',line).group(1)
				getMethod = True
			
			if "@PostMapping" in line:
				if "path" in line:
					apiPath = re.search('.*\{"(.*)"\}.*',line).group(1)
				else:
					apiPath = re.search('.*"(.*)".*',line).group(1)
				postMethod = True
			
			if "@PreAuthorize" in line:
				requiresLogin = True
			
			if getMethod or postMethod:
				if "public" in line:

					if re.match('\s+public\s(.*?)\s.*?\((.*)\).*?\{\s*', line):
						result = re.search('\s+public\s(.*?)\s.*?\((.*)\).*?\{\s*', line)
						returnType = result.group(1)
						parameters = result.group(2)
				
						printApiDefinition(parameters, returnType)
						resetMethodParseState()
					else:
						result = re.search('\s+public\s(.*?)\s.*?\((.*),', line)
						returnType = result.group(1)
						parameters = result.group(2)
						multiLineParam = True
						
				elif multiLineParam:
					if re.match('\s+(.*)\).*?\{\s*', line):
						result = re.search('\s+(.*)\).*?\{\s*', line)
						parameters += ", "+result.group(1)
					
						printApiDefinition(parameters, returnType)
						resetMethodParseState()
					else:
						result = re.search('\s+(.*),\s*', line)
						parameters += ", "+result.group(1)

	file.close()

print("")
print("Processing complete.  Total {0} APIs found".format(numApisFound))