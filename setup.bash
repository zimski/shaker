echo "# Install REDIS and nodejs"
apt-get install update
apt-get install redis-server
apt-get install nodejs

echo "# Install Python"
apt-get install python
apt-get install python-pip
pip install redis
pip install paramiko
pip install scp
pip install yaml
pip install Mako
pip install socketIO-client
pip install pexpect
echo "# Set password for Shaker"
redis-cli hmset shaker:login user admin pass 21232f297a57a5a743894a0e4a801fc3
