import urllib
import urllib2
import nsGlobal
import time
def run(ssh,prgm,sk):
    script = prgm['script']
    argv = prgm['argv']
    nsGlobal.continue_cmd = prgm['wait']

    post_data = urllib.urlencode({'argv':argv,'father_id': nsGlobal.self_id});
    request = urllib2.Request('http://'+prgm['host']+':'+str(prgm['port'])+'/run_shaker/'+script,post_data)
    sk(3,'Send request to server: '+script)
    response = urllib2.urlopen(request)
    data_rt = response.read()
    sk(2,data_rt)
    while nsGlobal.continue_cmd:
        time.sleep(0.5) 
    print "run finish !"
