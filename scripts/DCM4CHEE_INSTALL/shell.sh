dcm4chee_exist=`dpkg --list | grep dcm4chee | wc -l`
$$ sk_console.get DCM
## test if dcm4chee is installed
$$ rbox.cmd_if COND
## run dcm4chee
/etc/rc.local start


