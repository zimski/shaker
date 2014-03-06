import yaml
from mako.template import Template
from socketIO_client import SocketIO
import redis,sys

r = redis.StrictRedis()
socketIO = SocketIO('localhost', 3002)
import pxssh
import getpass
#import pexpect

# import custom module
from modules import *

import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


WEB_CONSOLE= True

def web_console_cmd(data):
  if WEB_CONSOLE:
    socketIO.emit('console-emit-cmd','<span class="console-cmd">[#]'+str(data)+'</span>\n')
  else:
    print '[#]'+str(data)

def web_console_rt(data):
  if WEB_CONSOLE:
    socketIO.emit('console-emit',str(data))
  else:
    print '[#]'+str(data)


def web_console_info(data):
  if WEB_CONSOLE:
    socketIO.emit('console-emit-cmd','<span class="console-cmd msg">[#]'+str(data)+'</span>\n')
  else:
    print '[#]'+str(data)

# cmd to run a custom command (call to python module)
def run_cmd(ssh,data,cmd):
  # extract cmd and arguments
  tmp1_ = cmd.split(' ')
  print tmp1_
  module_name_methode = tmp1_[1]
  tmp2_ = module_name_methode.split('.')
  module_name = tmp2_[0]
  methode_name = tmp2_[1]
  # argumet
  arguments =tmp1_[2]
  
  # run the commande
  cmd_to_run = module_name+'.'+methode_name+'(ssh,data["'+arguments+'"])'
  web_console_info("[$$] call module : "+cmd_to_run)
  web_console_info("[$$] ...")
  print cmd_to_run
  with stdoutIO() as s:
    exec cmd_to_run
  web_console_info("[#] module finish : "+s.getvalue())

def ssh_cmd(cmds,var):
  try:
    s = pxssh.pxssh()
    hostname = var['script']['host'] 
    username = var['script']['user'] 
    password = var['script']['password']
    s.login(hostname, username, password)
    
    for cmd in cmds:
      web_console_cmd(cmd)
      # looking for the cmd balise .... must be in the begining of the line
      
      if cmd.find('$$')==0 :
        run_cmd(s,var,cmd)
        continue
      
      s.sendline(cmd)
      s.prompt()
      message_rt = s.before
      if message_rt.find("[Y/n]?") != -1 or message_rt.find("[O/n]?") !=-1 :
        web_console_info("[!] i confirm Yes")
        s.sendline("Y")
        s.prompt()
     
      web_console_rt(s.before)
    web_console_info("Script complete")
  except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)
    web_console_info('[!!!] ERROR:'+str(e))




tmp = Template(filename='env.yaml')
data =[]
data.append('machine-test-salt-shaker')
data_var_env = yaml.load(tmp.render(args_env=data))
print data_var_env
print "parsing script"

tmp_sc = Template(filename='script_exec.bash')
sc_content = tmp_sc.render(env=data_var_env)
print "# code shell"

list_cmd = sc_content.split('\n')
#print list_cmd
# run command SSH
ssh_cmd(list_cmd,data_var_env)

