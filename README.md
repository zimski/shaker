![alt tag](https://github.com/zimski/shaker/raw/master/public/images/sk1.png)
Automation CMS to create and manage modules to do automated task from web interface

## how ?
Bash with python/mako layer.
With Shaker web interface you can edit your shell and variable environment file, you can also check syntax and run it.

With Shaker, you can manage your IT infrastructure, configure and create VM from any HyperViseur,
push conf on your Networks devices.

The strangth point of shaker is his ability to make your own modules with your own script via the web interface


## Install Shaker

```bash
git clone https://github.com/zimski/shaker.git
cd shaker && sudo bash setup.bash
``` 
please check if the version of node installed >= v0.10.XX
if not, install NVM and get v0.10

https://github.com/creationix/nvm

```
curl https://raw.github.com/creationix/nvm/v0.3.0/install.sh | sh
(( reopen the terminal ))
nvm install 0.10
node app

```
## Configuration

Go to shaker/py-sc/shaker.conf and edit with a valid account, this account will be used to ssh your localhost (if it's needed)
You can create a dedicated user for shaker, in this case you will able to control shaker permissions

change also the "pwd" with the curent shaker folder in your machine

```yaml
localhost:
    user : shaker
    password: shakerpass@
pwd : /home/shaker
```

## Start Shaker

```bash
node app.js
```
You can access to Shaker at this address : __http://localhost:3002/__
```
user :      admin
password :  admin
```
## Example of Shaker Script
We have two files, the env file, where we fetch our variables, we can use Python code to fetch and Mako to template the file
the second file is the bash script,

### Full Proxmox create vm example:
In this case, we have a Proxmox cluster and a Shaker machine, we will run this script in the shaker machine,
Shaker will perform an ssh to the Proxmox cluster and run our commands
#### env file
```python
<%
  import redis
  r = redis.StrictRedis()
  data = r.hgetall(argv[0]) ## we get data from REDIS  DB, argv[] it's shaker parameters
  ## data its a dictionnary
  ## data = {ip : IP,mac : MAC , vmid: ID,..}
%>
script:
  host  : 192.168.0.8 # proxmox machine
  user  : root
  password  : cspolperdio

vm:
  mac       : ${data['mac'].upper()}
  # we can have vm paramters like cpu ram image ...ect

GET_VAR:
    - NEXT_VMID

UPDATE_VM_ID:
    code: |
        import redis
        r = redis.StrictRedis()
        r.hset('${argv[0]}','vmid',NEXT_VMID)
        print "update vm !"
```
#### shell file
```bash
NEXT_VMID=$(pvesh get cluster/nextid | sed 's/"//g')
mkdir /var/lib/vz/images/$NEXT_VMID
cp /var/lib/vz/images/111/base-111-disk-1.qcow2 /var/lib/vz/images/$NEXT_VMID/base-$NEXT_VMID-disk-1.qcow2
pvesh create /nodes/proxmox/qemu -vmid $NEXT_VMID -memory 2048 -sockets 1 -cores 2 -net0 e1000=${env['vm']['mac']},bridge=vmbr0 -ide0=local:$NEXT_VMID/base-$NEXT_VMID-disk-1.qcow2
echo "vm created"
$$ sk_console.get GET_VAR ## get variable from Proxmox machine
$$ rbox.py_run UPDATE_VM_ID ## update in our DB the curent VM_ID of the virtual machine
sleep 5 ; pvesh create /nodes/proxmox/qemu/$NEXT_VMID/status/start
```
we can call to internal shaker module with "$$", it's very easy to add new modules to shaker, you just have to add a python code in py-sc/modules/yourfile and add the name of your file in "\_\_init__.py"
#### run it !
+ from terminal
```
python shaker.py -x -e <path to env file> -s <path to shell file>
```
+ from web interface
![alt tag](https://github.com/zimski/shaker/raw/master/public/images/sk_run.png)


## to be continued ...
