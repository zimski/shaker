apt-get update
apt-get install curl
echo "${env['global_var']['hostname']}" > /etc/hostname
/etc/init.d/hostname start
hostname ${env['global_var']['hostname']}
curl -L http://bootstrap.saltstack.org | sh
hostname
hostname -f
$$ send_file.send file_conf_salt_minion
## send hosts file 
$$ send_file.send file_hosts
cat /etc/salt/minion
/etc/init.d/salt-minion restart