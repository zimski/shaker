import yaml
import os
from mako.template import Template
from socketIO_client import SocketIO,BaseNamespace
import redis,sys,getopt,pxssh,getpass,StringIO,contextlib,pexpect
from threading import Thread
# import custom module
from modules import *
r = redis.StrictRedis()
nsGlobal.init()
class Namespace(BaseNamespace):
    def on_halt(self,args):
        nsGlobal.halt = True;
        sys.exit(0)

    def on_register(self,args):
        print "registerrr"
        nsGlobal.self_id = args['id']
        print "My ID "+str(args['id'])
        print "My father ID "+str(nsGlobal.father_id)
    def on_connect(self):
        print '[Connected]'
    def on_finish(self,args):
        socketIO.emit('console-emit-cmd','<span class="console-cmd">\
                [#]FiniSH recu '+str(args['father_id'])+' |'+\
                str(nsGlobal.self_id)+'</span>\n')
        if int(args['father_id']) == nsGlobal.self_id :
               socketIO.emit('console-emit-cmd','<span class="console-cmd">\
                       [#]FiniSH recu OK '+str(args['father_id'])+'</span>\n')
               nsGlobal.continue_cmd = False
socketIO = SocketIO('localhost', 3002,Namespace)
thread = Thread(target= socketIO.wait)
thread.setDaemon(True)
thread.start()




@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

## ============  Event of socket  ========
#def on_register(*args):
#    print "registerrrr   "+str(args.id)
#socketIO.on('register',on_register)
## =======================================
WEB_CONSOLE= False
mode =0
def emit_son_finish():
  socketIO.emit("finish",{"father_id":nsGlobal.father_id})

def web_console_cmd(data):
  if WEB_CONSOLE:
    socketIO.emit('console-emit-cmd',\
            '<span class="console-cmd">[#]'+str(data)+'</span>\n')
  else:
    print '[#]'+str(data)

def web_console_rt(data):
  if WEB_CONSOLE:
    socketIO.emit('console-emit',str(data))
  else:
    print '[#]'+str(data)


def web_console_info(data):
  if WEB_CONSOLE:
    socketIO.emit('console-emit-cmd',\
            '<span class="console-cmd msg">[#]'+str(data)+'</span>\n')
  else:
    print '[#]'+str(data)
def web_console(mode,data):
    if mode ==1:
        web_console_cmd(data)
    if mode ==2:
        web_console_rt(data)
    if mode ==3:
        web_console_info(data)
    if mode == 10:
        emit_son_finish()
    if mode == 99:
        socketIO.emit('halt',{})
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
  cmd_to_run = module_name+'.'+methode_name+'(ssh,data["'+arguments+'"],web_console)'
  if mode != 1:
    web_console_info("[$$] call module : "+cmd_to_run)
    web_console_info("[$$] ...")
  if mode ==1:  
    print '[debug][cmd to run]'+cmd_to_run
  else:
    with stdoutIO() as s:
      exec cmd_to_run
    web_console_info("[#] module finish ["+arguments+"] : "+s.getvalue())

def ssh_cmd(cmds,var):
  global mode
  try:
    s = pxssh.pxssh()
    hostname = var['script']['host'] 
    username = var['script']['user'] 
    password = var['script']['password']
    if mode !=1:
      s.login(hostname, username, password)
    inside_block = False
    s.sendline()
    i = s.expect([pexpect.EOF,s.PROMPT])
    #while i !=1:
    #    s.logout()
    #    s.login(hostname,username,password)
    #    i =s.expect(pexpect.EOF,s.PROMPT)
    for cmd in cmds:
      # Check if we must halt ?!!!
      if nsGlobal.halt:
          web_console_info("["+str(nsGlobal.self_id)+"]  **** Halted ****")
          s.logout()
          sys.exit(0)
      # looking for the cmd balise .... must be in the begining of the line
      
      if cmd.find('$$')==0 :
        run_cmd(s,var,cmd)
        continue
      if cmd.find('$<')==0:
        inside_block = True
        continue
      if cmd.find('$>')==0:
        inside_block = False
        s.prompt()
        message_rt = s.before
        web_console_rt(message_rt)
        continue 
      if mode ==1:
        continue
      
      s.sendline(cmd)
      if mode !=1:
        web_console_cmd(cmd)
      if inside_block == False:  
        s.prompt()
        message_rt = s.before
        web_console_rt(message_rt)
     
      
           
   
    web_console_info("Script complete")
    s.logout()

  except Exception as e:
    print("SSH error.")
    print(e)
    web_console_info('[!!!] SSH ERROR:'+str(e))
    # Send a Halt to stop every things
    web_console_cmd(' ERROR ::::: SEND HALT TO ALL PROCESS :::::::')
    socketIO.emit('halt-error',{})

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
    opts,args = getopt.getopt(argv,'hdxwe:s:',\
            ['env_file=','shell_file=','argv=','father_id='])
  except getopt.GetoptError:
    print '\t usage: shaker.py -[d|x|w] -e <file_env> \
            -s <file_shell> --argv=<arg1 arg2 ...>'
    sys.exit(2)
  for opt,arg in opts:
    if opt =='-h':
      print '\nusage : shaker.py -[d|x] \
              -e <file_env> -s <file_shell> --argv=<arg1 arg2 ...>\n'
      print '\t-d\t\tMode Debug, check templating result'
      print '\t-w\t\tSend notification to webGUI'
      print '\t-x\t\tRun script'
      print '\t-e <file>\tSet file env variables'
      print '\t-s <file>\tSet script file'
      print '\t--argv=<args>\tSet arguments\n'
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
    elif opt == '--father_id':
      nsGlobal.father_id = arg
  if mode ==1:
    print '\t\t[Shaker Debug]\n'
  nsGlobal.mode = mode
  # Parsing shaker config
  #LOCAL_PATH=os.path.realpath(__folder__)
  LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
  conf_file = open(LOCAL_PATH+'/shaker.conf','r')
  SHAKER_CONF = yaml.load(conf_file)
  # parsing env.yaml
  if env_file != '':
    if mode ==1:
      print '\t\t[debug][env yaml]\n'
    tmp = Template(filename=env_file)
    
    
   # data.append('IRCWWP001')
    print 'console arg'
    print console_arguments
    try:
        str_yaml = tmp.render(argv=console_arguments,shaker=SHAKER_CONF)
    except Exception as e:
        print "Yaml Parse env error "+str(e)
        if str(e).find("list index out of range")>=0:
            print "[shaker] please insert arguments,\
                    your yaml need arguments to be set arg[]"
        sys.exit(2)
    if mode ==1:
      print '[debug][content of env]:'
      print  str_yaml
      print '[debug][end content of env]'
    data_var_env = yaml.load(str_yaml)
  
  # Update nsGlobal
  nsGlobal.env = data_var_env
  # parsing shell

  if shell_file == '':
    print "Erreur: No shell file set"
    sys.exit(2)
  if mode ==1:
    print '\n\n'
    print '\t\t[debug][~ shell ~]\n'
  tmp_sc = Template(filename=shell_file)
  try:
    sc_content = tmp_sc.render(env=data_var_env)
  except Exception as e:
    print 'Yaml parse shell error '+str(e)
  if mode ==1:
    print '[debug][content of shell]\n'
    print sc_content
    print '[debug][end content of shell]\n'
  list_cmd = sc_content.split('\r\n')
  print list_cmd
  # run command SSH
  ssh_cmd(list_cmd,data_var_env)
  if nsGlobal.father_id !=0:
    emit_son_finish() 
  exit(0)
if __name__ == "__main__":
   main(sys.argv[1:])
