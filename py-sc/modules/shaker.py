import urllib
import urllib2
import nsGlobal
import time
def run(ssh,prgm,sk):
    script = prgm['script']
    argv = prgm['argv']
    nsGlobal.continue_cmd = prgm['wait']
    if nsGlobal.continue_cmd:
        post_data = urllib.urlencode({'argv':argv,'father_id': nsGlobal.self_id});
    else:
        post_data = urllib.urlencode({'argv':argv,'father_id': 0});

    request = urllib2.Request('http://'+prgm['host']+':'+str(prgm['port'])+'/run_shaker/'+script,post_data)
    sk(3,'Send request to server: '+script)
    response = urllib2.urlopen(request)
    data_rt = response.read()
    sk(2,data_rt)
    while nsGlobal.continue_cmd and not nsGlobal.halt:
        time.sleep(0.5) 
    print "run finish !"
def stop(ssh,prgm,sk):
    sk(10,'Stop from command')
    nsGlobal.halt = True
def stop_all(ssh,prgm,sk):
    sk(99,'Stop All from command')
    nsGlobal.halt = True
