#!/usr/bin/env python

'''
								Requirments 

git should be installed and password less access to the repo to clone has to be enabled 

'''
import os
from os.path import isfile, join
import requests 
import subprocess
import shutil
import sys

#folder="DEV"
#git_url="git@gitlab.zycus.com:root/iRequest.git"
#git_tag="17.59.1.0_Dev_iRequest"
#consul_ip='10.70.1.105'
#consul_port='8500'

git_url = sys.argv[1]
git_tag = sys.argv[2]
folder = sys.argv[3]
consul_ip = sys.argv[4]
consul_port = sys.argv[5]

def pull_from_git(git_tag,folder,git_url):
	
	git_clone=["git","clone","-b",git_tag,git_url,git_tag]
	try:
		subprocess.check_call(git_clone)
	except subprocess.CalledProcessError as e:
 		raise Exception("ERROR :: Please check the git repo URL or the input tag - %s " % e)
	path= os.getcwd()+'/'+folder
	try:
		properties_files = [f for f in os.listdir(path) if isfile(join(path, f))]
		if not properties_files:
			raise Exception("ERROR :: The input folder %s is either empty or doesn't exist" % folder)
	except NameError as e :
		raise Exception("ERROR :: The input folder %s is either empty or doesn't exist" % folder)
	except OSError as e :
		raise Exception("ERROR :: The input folder %s is either empty or doesn't exist" % folder)

	return properties_files

def load_properties(git_tag,folder,properties_files):
	data = {}
	for file in properties_files:
		file_name=file.split('.')[0]
		file_path=os.getcwd()+'/'+folder+'/'+file
		with open(file_path, "rt") as f:
			for line in f:
				key_value=line.split('=')
				key=folder+'/'+file_name+'/'+key_value[0].strip()
				value='='.join(key_value[1:]).strip().strip('"')
				data[key]=value
	return data

def insert_to_git(key_values,consul_ip,consul_port):
	counsul_base_address='http://'+consul_ip+':'+consul_port+'/v1/kv/'
	for keyVal in key_values:
		counsul_address=counsul_base_address+keyVal
		r=requests.put(counsul_address, data = key_values[keyVal])
		r.raise_for_status()

#def clear_repo(git_tag):
#	path=os.getcwd()+'/'+git_tag
#	shutil.rmtree(path)

def main():
	properties_files=pull_from_git(git_tag,folder,git_url)
	key_values=load_properties(git_tag,folder,properties_files)
	insert_to_git(key_values,consul_ip,consul_port)
	#clear_repo(git_tag)

if __name__=='__main__':
	main()
