$$ sk_ssh.expect CMD_accept
sleep 4
salt '${env['machine']}' test.ping
salt '${env['machine']}' state.highstate