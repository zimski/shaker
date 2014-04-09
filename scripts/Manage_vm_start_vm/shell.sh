ssh-keygen -f "/root/.ssh/known_hosts" -R ${env['vm']['ip']}
$$ shaker.run SCR_DHCP
% if env['vm']['type'] == 'VM' :
$$ shaker.run SCR_Proxmox
sleep 20
% endif
((count = 100)) # Maximum number to try.
$<
while [[ $count -ne 0 ]] 
do  
ping -c 3 ${env['vm']['ip']};
rc=$?; 
if [[ $rc -eq 0 ]] ; then ((count = 1)); fi; ((count = count - 1)); 
done
$>
$$ sk_console.get RC
$$ rbox.cmd_if CONDITION
##