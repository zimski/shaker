apt-get update
apt-get install curl
echo "${env['global_var']['hostname']}" > /etc/hostname
/etc/init.d/hostname start
hostname ${env['global_var']['hostname']}
curl -k -L http://bootstrap.saltstack.org | sh
hostname
$$ send_file.send file_conf_salt_minion
## send hosts file 
$$ send_file.send file_hosts
/etc/init.d/salt-minion restart
echo "helloo"