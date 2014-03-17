import nsGlobal
def ns_variabe(ssh,data,sk):
     
    for key,val in data.iteritems():
        nsGlobal.console[key]=val
        sk(3,'console NS: '+key+' :'+str(val))
def set(ssh,data,sk):
    for key,var in data.iteritems():
        cmd = key+'="'+str(var)+"\""
        ssh.sendline(cmd)
        ssh.prompt()
        sk(3,'SET '+key+' : '+str(var))

def get(ssh,var,sk):
    for k in var:
        cmd = 'echo $'+k
        ssh.sendline(cmd)
        ssh.prompt()
        data=ssh.before.replace(cmd+'\r\n','')
        nsGlobal.console[k]= data[:-2]
        sk(3,k+' = '+data[:-2])
    
