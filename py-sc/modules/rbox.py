import sys,StringIO,contextlib
import nsGlobal
import sk_console
import netDevice
import send_file
import sk_ssh
import shaker
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def py_run(ssh,script,sk):
    global console
    with stdoutIO() as s:
      exec script['code'] in nsGlobal.console
    sk(2,s.getvalue())

def cmd_if(ssh,code,sk):
   condition = False
   exec "condition=("+str(code['if'])+")" in nsGlobal.console
   if nsGlobal.console['condition']:
     cmds = code['then'].split('\n')
     ssh_cmd(ssh,cmds,nsGlobal.env,sk)
   else:
     cmds = code['else'].split('\n')
     ssh_cmd(ssh,cmds,nsGlobal.env,sk)

        
    
def run_cmd(ssh,data,cmd,sk):
  mode =nsGlobal.mode
  # extract cmd and arguments
  tmp1_ = cmd.split(' ')
  
  module_name_methode = tmp1_[1]
  tmp2_ = module_name_methode.split('.')
  module_name = tmp2_[0]
  methode_name = tmp2_[1]
  # argumet
  arguments =tmp1_[2]
  
  # run the commande
  if module_name =='rbox':
      cmd_to_run = methode_name+'(ssh,data["'+arguments+'"],sk)'
  else:
      cmd_to_run = module_name+'.'+methode_name+'(ssh,data["'+arguments+'"],sk)'

  if mode != 1:
    sk(3,"[$$] call module : "+cmd_to_run)
    sk(3,"[$$] ...")
  if mode ==1:  
    print '[debug][cmd to run]'+cmd_to_run
  else:
    with stdoutIO() as s:
      exec cmd_to_run
    sk(3,"[#] module finish ["+arguments+"] : "+s.getvalue())


def ssh_cmd(ssh,cmds,var,sk):
  mode= nsGlobal.mode
  try:
    inside_block = False

    for cmd in cmds:
    # Check if we must halt ?!!!
      if nsGlobal.halt:
          sk(3,"["+str(nsGlobal.self_id)+"]  **** Halt ****")
          ssh.logout()
          sys.exit(0)
     # looking for the cmd balise .... must be in the begining of the line
      
      if cmd.find('$$')==0 :
        run_cmd(ssh,var,cmd,sk)
        continue
      if cmd.find('$<')==0:
        inside_block = True
        continue
      if cmd.find('$>')==0:
        inside_block = False
        shh.prompt()
        message_rt = shh.before
        sk(2,message_rt)
        continue 
      if mode ==1:
        continue
      
      ssh.sendline(cmd)
      if mode !=1:
        sk(1,cmd)
      if inside_block == False:  
        ssh.prompt()
        message_rt = ssh.before
        sk(2,message_rt)
     
      
           
     
    sk(3,"Script complete")
  except Exception as e:
    print("SSH error.")
    print(e)
    sk(3,'[!!!] SSH ERROR:'+str(e))


