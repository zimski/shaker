import yaml
from mako.template import Template
from socketIO_client import SocketIO
import redis,sys,getopt,pxssh,getpass,StringIO,contextlib

r = redis.StrictRedis()
socketIO = SocketIO('localhost', 3002)

# import custom module
from modules import *


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


WEB_CONSOLE= False
mode =0
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
  global mode
  # extract cmd and arguments
  tmp1_ = cmd.split(' ')
  
  module_name_methode = tmp1_[1]
  tmp2_ = module_name_methode.split('.')
  module_name = tmp2_[0]
  methode_name = tmp2_[1]
  # argumet
  arguments =tmp1_[2]
  
  # run the commande
  cmd_to_run = module_name+'.'+methode_name+'(ssh,data["'+arguments+'"])'
  if mode != 1:
    web_console_info("[$$] call module : "+cmd_to_run)
    web_console_info("[$$] ...")
  if mode ==1:  
    print '[debug][cmd to run]'+cmd_to_run
  else:
    with stdoutIO() as s:
      exec cmd_to_run
    web_console_info("[#] module finish : "+s.getvalue())

def ssh_cmd(cmds,var):
  global mode
  try:
    s = pxssh.pxssh()
    hostname = var['script']['host'] 
    username = var['script']['user'] 
    password = var['script']['password']
    if mode !=1:
      s.login(hostname, username, password)
    
    for cmd in cmds:
      
      # looking for the cmd balise .... must be in the begining of the line
      
      if cmd.find('$$')==0 :
        run_cmd(s,var,cmd)
        continue
      
      if mode ==1:
        continue
      
      s.sendline(cmd)
      if mode !=1:
        web_console_cmd(cmd)
      s.prompt()
      message_rt = s.before
            
     
      
      web_console_rt(message_rt)
     
      
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

#---------------------------------
#                 MAIN
#---------------------------------

def main(argv):
  env_file = ''
  shell_file = ''
  console_arguments =[]
  # mode
  # 1 : debug
  # 2 : execute
  global mode
  #print argv
  mode = 0 
  global WEB_CONSOLE
  try:
    opts,args = getopt.getopt(argv,'hdxwe:s:',['env_file=','shell_file=','argv='])
  except getopt.GetoptError:
    print 'shaker.py -[d|x|w] -e <file_env> -s <file_shell> --argv=<arg1 arg2 ...>'
    sys.exit(2)
  for opt,arg in opts:
    if opt =='-h':
      print 'shaker.py -[d|x] -e <file_env> -s <file_shell>'
      sys.exit(2)
    elif opt in ('-e','--env_file'):
      env_file = arg
    elif opt in ('-s','--shell_file'):
      shell_file = arg
    elif opt =='-d':
      mode =1
    elif opt == '-x':
      mode =2
    elif opt =='-w' :
      WEB_CONSOLE = True
    elif opt == '--argv':
      console_arguments = arg.split()
  if mode ==1:
    print '\t\t[Shaker Debug]\n'
  # parsing env.yaml
  if env_file != '':
    if mode ==1:
      print '\t\t[debug][env yaml]\n'
    tmp = Template(filename=env_file)
    
    
   # data.append('IRCWWP001')
    print 'console arg'
    print console_arguments
    str_yaml = tmp.render(argv=console_arguments)
    if mode ==1:
      print '[debug][content of env]:'
      print  str_yaml
      print '[debug][end content of env]'
    data_var_env = yaml.load(str_yaml)
   
  # parsing shell
  if shell_file == '':
    print "Erreur: No shell file set"
    sys.exit(2)
  if mode ==1:
    print '\n\n'
    print '\t\t[debug][~ shell ~]\n'
  tmp_sc = Template(filename=shell_file)
  sc_content = tmp_sc.render(env=data_var_env)
  if mode ==1:
    print '[debug][content of shell]\n'
    print sc_content
    print '[debug][end content of shell]\n'
  list_cmd = sc_content.split('\r\n')
  #print list_cmd
  # run command SSH
  ssh_cmd(list_cmd,data_var_env)

if __name__ == "__main__":
   main(sys.argv[1:])
