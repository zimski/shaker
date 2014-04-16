$!+ rbox.cmd_if CC
VARIF=100
echo "1"
$!+ rbox.cmd_if CC
echo "2"
echo "3"
$$ shaker.stop_all
$$ sk_console.get VAR
$$ rbox.cmd_if CONDITION
echo "hello 3333"