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
def set_from_ns(ssh,data,sk):
    for key in data:
        if isinstance(nsGlobal.console[key],(int,long)):
            cmd = key+'='+str(nsGlobal.console[key])
        else:
            cmd = key+'="'+nsGlobal.console[key]+'"'
        ssh.sendline(cmd)
        ssh.prompt()
        sk(3,'SET '+key+' : '+str(nsGlobal.console[key]))


def get(ssh,var,sk):
    for k in var:
        cmd = 'echo $'+k
        ssh.sendline(cmd)
        ssh.prompt()
        data=ssh.before.replace(cmd+'\r\n','')
        data_geted =data[:-2]
        try:
            val = int(data_geted)
            nsGlobal.console[k]= val
            sk(3,k+' = '+data[:-2]+'  ((INT))')
        except:
            nsGlobal.console[k] = data_getted
            sk(3,k+' = '+data[:-2]+'  ((STR))')
    
