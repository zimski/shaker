echo "hellooo"
LOCAL_VAR="hollallalalala from 192.168.0.144"
## set variables on the remote terminal
$$ sk_console.set VAR
echo $COUCOU
## get variables from the remote terminal
$$ sk_console.get VAR1
## run a simple python script and use those variables
$$ rbox.py_run CODE1
## set variables maked from the python script and save theme on the remote terminal
$$ sk_console.set_from_ns VAR2
echo $f
echo "good"