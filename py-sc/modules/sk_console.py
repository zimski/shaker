console={}
def ns_variabe(ssh,data,sk):
    global console
    for key,val in data.iteritems():
        console[key]=val
        sk(3,'console NS: '+key+' :'+str(val))
def set(ssh,data,sk):
    global console
    for key,var in data.iteritems():
        cmd = key+'="'+str(var)+"\""
        ssh.sendline(cmd)
        ssh.prompt()
        sk(3,'SET '+key+' : '+str(var))

def get(ssh,var,sk):
    global console
    for k in var:
        cmd = 'echo $'+k
        ssh.sendline(cmd)
        ssh.prompt()
        data=ssh.before.replace(cmd+'\r\n','')
        console[k]= data[:-2]
        sk(3,k+' = '+data[:-2])
    
