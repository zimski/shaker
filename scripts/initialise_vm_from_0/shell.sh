wget http://192.168.0.222:3002/run_shaker/update_dhcp-vm --post-data=""
wget http://192.168.0.222:3002/run_shaker/Proxmox_create_vm --post-data="argv=${env['proxmox']['machine']}"
sleep 30; wget http://192.168.0.222:3002/run_shaker/script_file --post-data="argv=${env['proxmox']['machine']}"