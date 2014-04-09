import pxssh
import nsGlobal
import sys
def push(ssh,data,sk):
    netssh = pxssh.pxssh()
    user = data['user']
    password = data['password']
    hostname = data['hostname']
    netssh.login(hostname,user,password,auto_prompt_reset=False)
    list_cmd = data['conf'].split('\n')
    for cmd in list_cmd:
      # Check if we must halt ?!!!
      if nsGlobal.halt:
          sk(3,"["+str(nsGlobal.self_id)+"]  **** Halt ****")
          ssh.logout()
          sys.exit(0)
      netssh.sendline(cmd)
      sk(2,cmd+"\n")
    sk(3,'Push cmds finish ! :)')
