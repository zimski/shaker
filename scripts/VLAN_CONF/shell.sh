$$ sk_ssh.ssh SWITCH
$<
en
${env["conf"]["en_pass"]}
conf t
default interface ${env["conf"]['int']}

% if env["conf"]["voip"]== False :
interface ${env["conf"]['int']}
description ${env["conf"]['description']}
switchport access vlan ${env["conf"]['vlan']}
switchport mode access
switchport nonegotiate
no cdp enable
spanning-tree portfast
spanning-tree bpduguard enable

% else :

interface ${env["conf"]['int']}
description ${env["conf"]['description']}
switchport access vlan ${env["conf"]['vlan']}
switchport mode access
switchport nonegotiate
switchport voice vlan 224
srr-queue bandwidth share 10 10 60 20
queue-set 2
priority-queue out
mls qos trust device cisco-phone
mls qos trust dscp
auto qos voip cisco-phone
spanning-tree portfast
spanning-tree bpduguard enable
service-policy input AutoQoS-Police-CiscoPhone
% endif
exit
exit
exit
$>
$exit
echo "======================== configuration finie =================================="