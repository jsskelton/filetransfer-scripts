#!/bin/env/python

"""
Pulls a text file from a server over ssh using sftp through paramiko. Not tested for binary files.
Requires the paramiko module to be installed on the machine running the script.
Only tested on paramiko 1.15.1
"""

import paramiko,sys,time,getopt,os,socket

fname = "tempout"
localpath = os.path.join(os.sep, 'tmp', fname + '.in')

#set up the ssh connection through paramiko
def setupClient(ip,user,passwd):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip,username=user,password=passwd,timeout=10)
	return client

#try to cat the contents of the file through the ssh connection
def getFile(client,filename):
        sftp = client.open_sftp()
        stdin, stdout, stderr = sftp.get(filename,localpath)
	temp = stderr.read()
	if temp != "":
		print "An error occured while trying to grab the file "+filename+":"
		print temp.strip()
		sys.exit(1)
        client.close()
                
def main(argv):
	if len(argv) == 0:
		print 'file_check.py -i <ip> -u <username> -p <password> -f <filename> -o <outfile>'
		sys.exit(2)
	try:
		opts,args = getopt.getopt(argv,"h:i:u:p:f:o:",["help=","ip=","username=","password=","filename=","outfile="])
	except getopt.GetoptError:
		print "Error in getting values from cmd"
		print 'file_check.py -i <ip> -u <username> -p <password> -f <filename> -o <outfile>'
		sys.exit(2)
	for opt,arg in opts:
		if opt in ('-h','--help'):
			print 'file_check.py -i <ip> -u <username> -p <password> -f <filename> -o <outfile>'
		elif opt in ('-i','--ip'):
			ip = arg
		elif opt in ('-u','--username'):
			user = arg
		elif opt in ('-p','--password'):
			passwd = arg
		elif opt in ('-f','--filename'):
			filename = arg
		elif opt in ('-o','--outfile'):
			outfile = arg
	try:
		client = setupClient(ip,user,passwd)
	except socket.timeout:
		print "timed out while trying to connect to "+ip
		sys.exit(1)
	except paramiko.ssh_exception.AuthenticationException:
		print "incorrect login credentials, check login credentials and try again"
		sys.exit(1)
	# output = checkFile(client,filename)
        print filename
        print localpath
        print os.path.isfile(localpath)
        print outfile
        print os.path.isfile(outfile)
#        if os.path.isfile(localpath):
#               if os.path.isdir(outfile):
#		        print "Unable to create output file because a folder with the same name currently exists"
#		        sys.exit(1)
#	        if os.path.isfile(outfile):
#		        print "A file with the name "+outfile+" currently exists, overwriting existing file"
#               os.system("cat -n " + localpath + "> "+outfile)
#        print "test output written to file "+outfile
#       else:
#              print os.path.isfile(outfile)
#               print "Input file "+filename+" was not copied for some reason"
#               sys.exit(1)        
	
if __name__ == "__main__":
	main(sys.argv[1:])  
