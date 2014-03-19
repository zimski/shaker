import pxssh

def pull(ssh,data,sk):
    netssh = pxssh.pxssh()
    user = data['user']
    password = data['password']
    hostname = data['hostname']
    netssh.login(hostname,user,password,auto_prompt_reset=False)
    list_cmd = data['conf'].split('\n')
    for cmd in list_cmd:
        netssh.sendline(cmd)
        sk(2,cmd+"\n")
    sk(3,'pull finish ! :)')
