wget http://192.168.0.222:3002/run_shaker/Manage_vm_update_dhcp --post-data=""
% if env['vm']['type'] == 'VM' :
wget http://192.168.0.222:3002/run_shaker/Proxmox_create_vm --post-data="argv=${env['proxmox']['machine']}"
sleep 20
% endif
((count = 100)) # Maximum number to try.
while [[ $count -ne 0 ]] ; do  ping -c 3 ${env['vm']['ip']};rc=$?; if [[ $rc -eq 0 ]] ; then ((count = 1)); fi; ((count = count - 1)); done
if [[ $rc -eq 0 ]] ; then wget http://192.168.0.222:3002/run_shaker/Manage_vm_conf_salt --post-data="argv=${env['proxmox']['machine']}"; else echo `Timeout Vm not run check network or proxmox`;fi