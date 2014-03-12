wget http://192.168.0.222:3002/run_shaker/update_dhcp-vm --post-data=""
wget http://192.168.0.222:3002/run_shaker/Proxmox_create_vm --post-data="argv=${env['proxmox']['machine']}"
sleep 20
((count = 100)) # Maximum number to try.
while [[ $count -ne 0 ]] ; do  ping -c 3 ${env['vm']['ip']};rc=$?; if [[ $rc -eq 0 ]] ; then ((count = 1)); fi; ((count = count - 1)); done
if [[ $rc -eq 0 ]] ; then wget http://192.168.0.222:3002/run_shaker/script_file --post-data="argv=${env['proxmox']['machine']}"; else echo `Timeout Vm not run check network or proxmox`;fi