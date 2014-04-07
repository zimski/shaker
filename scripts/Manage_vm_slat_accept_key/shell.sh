minion_exist=`salt-key | grep -Fx '${env['machine']}' | wc -l`
nb_try=0
$$ sk_console.get DCM
$$ rbox.cmd_if COND

