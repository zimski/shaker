import urllib
import urllib2

def run(ssh,prgm,sk):
    script = prgm['script']
    argv = prgm['argv']
    post_data = urllib.urlencode({'argv':argv});
    request = urllib2.Request('http://'+prgm['host']+':'+str(prgm['port'])+'/run_shaker/'+script,post_data)
    sk(3,'Send request to server: '+script)
    response = urllib2.urlopen(request)
    data_rt = response.read()
    sk(2,data_rt)
    print "run finish !"
