from socketIO_client import SocketIO
import redis,sys

r = redis.StrictRedis()
socketIO = SocketIO('localhost', 3002)
import pxssh
import getpass
import pexpect
hostname = sys.argv[1]


data = r.hgetall(hostname)
print data

try:
    s = pxssh.pxssh()
    hostname = data['ip'] #"192.168.0.111" #raw_input('hostname: ')
    username = "root" #raw_input('username: ')
    password = data['pass']#"cspolperdio" #getpass.getpass('password: ')
    s.login(hostname, username, password)
    


    socketIO.emit('console-emit-cmd','<span class="console-cmd">[#] apt-get update</span>\n')
    s.sendline("apt-get update")
    s.prompt()
    print(s.before)
    socketIO.emit('console-emit',s.before)
    
    socketIO.emit('console-emit-cmd','<span class="console-cmd">[#] apt-get install curl</span>\n')
    s.sendline("apt-get install curl")
    
    s.prompt()
    message_rt = s.before
    if message_rt.find("[Y/n]?") != -1 :
      print "i confirm Yes"
      s.sendline("Y")
      s.prompt()
   
    print(s.before)
    socketIO.emit('console-emit',s.before)

    s.prompt()
    socketIO.emit('console-emit-cmd','<span class="console-cmd">[#] curl -L http://bootstrap.saltstack.org | sh</span>\n')
    s.sendline("curl -L http://bootstrap.saltstack.org | sh")
    s.prompt()
    print(s.before)
    socketIO.emit('console-emit',s.before)

    
    s.logout()
    socketIO.emit('console-emit-cmd','<span class="console-cmd msg" >[#] Initialisation complete\n')
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)
    socketIO.emit('console-emit',s.before)



