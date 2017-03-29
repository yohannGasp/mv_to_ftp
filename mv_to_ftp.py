#!/usr/bin/python
# -*- coding: utf-8 -*-

#===================================================================================================
#  Bank to FTP
#  
#  29.03.2017
#===================================================================================================

import time
import json
import os
import sys
import shutil

#===================================================================================================
#  Global parameters
#===================================================================================================

reload(sys)
sys.setdefaultencoding('utf8')
PATH_IN   = ''
PATH_OUT  = ''
mask      = ''

#===================================================================================================
#  Settings 
#===================================================================================================
try:

	conf = open('sett.conf','r')
	param = conf.read()
	js_param = json.loads(param)

	PATH_IN  = js_param['path_in']
	PATH_OUT = js_param['path_out']
	mask     = js_param['mask'] 
	SLEEP    = js_param['sleep']
	LOG      = js_param['log']
	FLAG     = js_param['flag']

	# print(PATH_IN)
	# print(PATH_OUT)
	# print(mask)
	# print(SLEEP)
	# print(LOG)
	
except ValueError:
	print("#==================================")
	print("#  error json")
	print("#==================================")

except FileNotFoundError :
	print("#==================================")
	print("# not file sett.conf")
	print("#==================================")

#===================================================================================================
# function find_files 
#===================================================================================================
def find_files():

	fl_error = False

	try:

		tree=os.walk(PATH_IN)		
		for current_dir, dirs, files in tree:
			for file in files:
				path = os.path.join(current_dir,file)
				target = PATH_OUT + current_dir[len(PATH_IN):]

				if not os.path.exists(target):
					os.makedirs(target)
					logs('makedir' + target)
				shutil.move(path, target)
				logs('move ' + path + ' in ' + target)

	except Exception as e:
		fl_error = True
		logs("error: {0}".format(e))

	if fl_error == False:
		tree=os.walk(PATH_IN)			
		for current_dir, dirs, files in tree:
			for dir_ in dirs:
				shutil.rmtree(os.path.join(current_dir,dir_))
				logs('rm ' + os.path.join(current_dir,dir_))

#===================================================================================================
# function logs 
#===================================================================================================
def logs(msg):
	try:
		log = open(str(LOG),'a')
		log.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' ' + msg + '\n')
	finally:
		log.close()


#===================================================================================================
#  Main
#===================================================================================================

if not os.path.exists(FLAG):
	logs('start')
	f = open(FLAG, 'w')  # lock
	find_files()
	os.remove(FLAG)	     # unlock
	logs('finish')