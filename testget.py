import paramiko
import os

paramiko.util.log_to_file('logfile.log')

host = "101.102.103.104"
port = 22
transport = paramiko.Transport((host, port))
password = "pass"
username = "user"
transport.connect(username = username, password = password)

sftp = paramiko.SFTPClient.from_transport(transport)

filepath = '~/remote/file'
localpath = '~/local/file'
sftp.get(filepath, localpath)

sftp.close()
transport.close()
