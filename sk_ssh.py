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
def expect(ssh,data):
    # send cmd
    ssh.send(data['cmd'])
    expect_list = []
    for (exp,cmd) in data['@'].items():
        expect_list.append(exp)
    expect_list.append(TIMEOUT)
    expect_list.append(ssh.PROMPT)
    exit_rt = len(expect_list)-2

    i= ssh.expect(expect_list,timeout=10)
    if i >= exit_rt:
        return "TIMEOUT"
    else:
        ssh.send(data['@'][expect_list[i]])
        return " get ["+expect_list[i]+"] => send [ "+(data['@'][expect_list[i]]+" ] "

