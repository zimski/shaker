#    DATA FORMAT
#
#file_conf_salt_minion:
#  host:
#    ip      :
#    user    :
#    password:
#  template:
#    file_name  :
#    dest_path  : 
#    var 1 :
#    var 2 :

import paramiko,os
from mako.template import Template
from scp import SCPClient

def render_file(data):
  tmp_file= Template(filename=data['template']['file_name'])
  return tmp_file.render(data=data['template'])

def send(ssh,data,sk):
  tmp_namefile = data['template']['file_name']+'.tmp'
  tmp_file = open(tmp_namefile,"w")
  tmp_file.write(render_file(data))
  tmp_file.close()
  
  
  try:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(data['host']['ip'],username=data['host']['username'],password=data['host']['password'])
    
    scp = SCPClient(ssh_client.get_transport())
    scp.put(tmp_namefile,data['template']['dest_path'])
    #os.remove(tmp_namefile)
    print " file send ...OK"
  except Exception as e:
    print "ERROR :"+str(e)

def test(ssh,data):
  print render_file(data)
