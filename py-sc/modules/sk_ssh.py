# Module to manage expect for ssh
#
# DATA Yaml
#
# cmd1:
#   cmd: "shell cmd"
#   @:
#     - "str1":"send1"
#     - "str2":"send2"
#
# At Prompt we quit the module and continue normal execution of bash
import pexpect
def expect(ssh,data,sk):
    # send cmd
    sk('module ssh:'+data['cmd'])
    ssh.sendline(data['cmd'])
    expect_list = []
    expect_list.append(ssh.PROMPT)
    for (exp,cmd) in data['expect'].iteritems():
        expect_list.append(exp)
    expect_list.append(pexpect.TIMEOUT)
    exit_rt = len(expect_list)-2
    while True:
        i= ssh.expect(expect_list,timeout=10)
        sk(ssh.before + "valeur i :"+str(i))
        if i == 0:
            print "PrompT"
            return 0
        else:
            ssh.sendline(data['expect'][expect_list[i]])
            sk(ssh.before)
            print " get [" + expect_list[i] + "] => send [ "+ data['expect'][expect_list[i]]+" ] "
