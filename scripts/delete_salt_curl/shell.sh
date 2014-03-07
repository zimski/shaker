% for paquet in ['salt-*','curl']:
apt-get remove ${paquet}
apt-get purge ${paquet}
% endfor

apt-get autoremove