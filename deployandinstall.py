import os
import paramiko
import sys, getopt

def main(argv):
   server = ''
   deployfile = ''
   location=''
   cmd=''
   ip=''
   username=''
   password=''
   
   
   try:
       opts, args = getopt.getopt(argv,"hs:d:l:c:i:u:p:",["server=","dfile=","location","command","ip","username","password"])
   except getopt.GetoptError:
      print 'deploy.py -s <server> -f <deployfile> -l <location> -c <command> -i <ip> -u <username> -p <password>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'deploy.py -s <server> -f <deployfile> -l <location> -c <command> -i <ip> -u <username> -p <password>'
         sys.exit()
      elif opt in ("-s", "--server"):
         server = arg
      elif opt in ("-d", "--dfile"):
         deployfile = arg
      elif opt in ("-l", "--location"):
         location = arg
      elif opt in ("-c", "--command"):
         cmd = arg
      elif opt in ('-i','--ip'):
 	 ip = arg
      elif opt in ('-u','--username'):
  	 user = arg
      elif opt in ('-p','--password'):
 	 passwd = arg         
         
   print 'server : ', server
   print 'deployment file : "', deployfile
   print 'location : ', location
   print 'command : ', cmd
   print 'ip : ', ip
   print 'username : ', username
   deploy (server,deployfile,location, cmd)

def deploy (s,d,l,i,u,p,x):
    lines =[]
    ssh = paramiko.SSHClient() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(s, username, passwd)
    sftp = ssh.open_sftp()
    sftp.get(d, l + os.path.basename(d))
#    sftp.put(d, l + os.path.basename(d))
    sftp.close()
    # Execute script
    stdin,stdout,stderr = ssh.exec_command(x)
    lines=stdout.readlines()
    # print stdout.readlines()
    
    for line in lines:
        print line
    ssh.close()

if __name__ == "__main__":
   main(sys.argv[1:])
