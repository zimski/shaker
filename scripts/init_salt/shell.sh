apt-get update
apt-get install curl
curl -L http://bootstrap.saltstack.org | sh
echo "${env['global_var']['hostname']}" > /etc/hostname
/etc/init.d/hostname.sh
hostname
hostname -f
$$ send_file.send file_conf_salt_minion 
cat /etc/salt/minion
/etc/init.d/salt-minion restart