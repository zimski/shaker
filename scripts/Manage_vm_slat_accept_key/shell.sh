sleep 5
$$ sk_ssh.expect CMD_accept
sleep 2
salt '${env['machine']}' test.ping
salt '${env['machine']}' state.highstate