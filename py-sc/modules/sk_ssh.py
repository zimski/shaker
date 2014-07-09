# Module to manage expect for ssh
#
# DATA Yaml
#
# cmd1:
#   cmd: "shell cmd"
#   expect:
#     - "str1":"send1"
#     - "str2":"send2"
#
# At Prompt we quit the module and continue normal execution of bash
import pexpect
def expect(ssh,data,sk):
    # send cmd
    sk(1,'module ssh:'+data['cmd'])
    ssh.sendline(data['cmd'])
    expect_list = []
    for (exp,cmd) in data['expect'].iteritems():
        expect_list.append(exp)
    expect_list.append(pexpect.TIMEOUT)
    expect_list.append(ssh.PROMPT)
    exit_rt = len(expect_list)-2
    while True:
        i= ssh.expect(expect_list,timeout=10)
        sk(2,ssh.before)
        if i >= exit_rt:
            print "PrompT or timeOut"
            return 0
       
        else:
            sk(2,ssh.before)
            ssh.sendline(data['expect'][expect_list[i]])
            sk(3,'I answer: '+data['expect'][expect_list[i]])
            print " get [" + expect_list[i] + "] => send [ "+ data['expect'][expect_list[i]]+" ] "
def ssh(ssh,data,sk):
    sk(1,'module ssh:'+data['cmd'])
    ssh.sendline(data['cmd'])
    
    user = data['user']
    password = data['password']
    prompt = True
    if "prompt" in data:
        prompt = data['prompt']

    expect_list = []
    expect_list.append("(?i)password:")
    expect_list.append("(?i)are you sure you want to continue connecting")
    expect_list.append(pexpect.TIMEOUT)
    if prompt:
        expect_list.append(ssh.PROMPT)
    exit_rt = len(expect_list)-2
    while True:
        i= ssh.expect(expect_list,timeout=10)
        sk(3,"rt "+str(i))
        sk(2,ssh.before)
        if i >= exit_rt:
            print "PrompT or timeOut"
            return 0
        else:
            if i == 1:
                ssh.sendline('yes')
            if i == 0 :
                ssh.sendline(password)
                sk(3,'I send password')
                if prompt:
                    ssh.set_unique_prompt()
                    sk(3,'set prompt !!')
                return 0
            
       

