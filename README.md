Shaker
======

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
