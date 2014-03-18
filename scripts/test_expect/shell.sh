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
## send scrip
$<
function setup() {
    mkdir -p $DBPATH
    echo "#Exporting db from the container to host, in $DBPATH"
    ID=$(sudo docker run -d $IMAGENAME /sbin/my_init --skip-startup-files --quiet)
    sudo docker cp $ID:/var/www/wallabag/db/poche.sqlite $DBPATH
    sudo chown -R $USER:$USER $DBPATH
    sudo chmod -R 777 $DBPATH
    ID=$(sudo docker stop $ID)
    ID=$(sudo docker rm $ID)
}
$>
setup ;
echo "good"