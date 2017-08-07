# Author: Ethical-H4CK3R
# Date: 08/07/17
# Description: Runs lighttpd server

import os
import time
import threading
import subprocess

lighttpd = '''# location of index.html
server.document-root="{}"  # path to index.html - path of lighttpd

# set permissions
server.modules = (
	"mod_access",
	"mod_alias",
	"mod_accesslog",
	"mod_fastcgi",
	"mod_redirect",
	"mod_rewrite"
	)

# php configs
fastcgi.server = ( ".php" => ((
		  "bin-path" => "/usr/bin/php-cgi",
		  "socket" => "/php.socket"
		)))

server.port = 80
server.pid-file = "/var/run/lighttpd.pid"

mimetype.assign = (
	".html" => "text/html",
	".htm" => "text/html",
	".txt" => "text/plain",
	".jpg" => "image/jpeg",
	".png" => "image/png",
	".css" => "text/css"
	)

static-file.exclude-extensions = (".fcgi", ".php", ".rb", "~", ".inc")
index-file.names = ("index.htm", "index.html")
'''.format(os.getcwd())

class Engine(object):
 def __init__(self):
  self.installing = False
  self.output = '.output.log'
  self.devnull = open(os.devnull,'w')

 def kill(self):
  subprocess.Popen('pkill lighttpd',shell=True).wait()
  subprocess.Popen("for task in `lsof -i :80\
  | grep -v 'COMMAND' | grep -v 'firefox-e' | awk '{print $2}'`;\
  do kill -15 $task;done",stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def lighttpdPath(self):
  return True if os.path.exists('/usr/sbin/lighttpd') else False

 def phpPath(self):
  return True if os.path.exists('/usr/bin/php7.0') else False


 def loading(self,msg):
  while self.installing:
   for n in range(4):
    if not self.installing:break
    subprocess.call('clear',shell=True)
    print 'Installing {} {}'.format(msg,n*'.')
    time.sleep(.4)

 def installLighttpd(self):
  self.installing = True
  threading.Thread(target=self.loading,args=['Lighttpd']).start()
  subprocess.Popen('apt-get install lighttpd -y',\
  stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  self.installing = False
  subprocess.call('clear',shell=True)
  if self.lighttpdPath():
   print 'Successfully Installed Lighttpd'
   time.sleep(3)
  else:
   exit('Failed To Install Lighttpd')

 def installPhp(self):
  self.installing = True
  threading.Thread(target=self.loading,args=['Php7.0']).start()
  subprocess.Popen('apt-get install php7.0-cgi -y',\
  stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  self.installing = False
  subprocess.call('clear',shell=True)
  if self.phpPath():
   print 'Successfully Installed Php7.0'
   time.sleep(3)
  else:
   exit('Failed To Install Php7.0')

 def lighttpdService(self):
  self.installPhp()
  self.installLighttpd()
  subprocess.Popen('service lighttpd restart',shell=True).wait()

 def lighttpdServer(self):
  log = open(self.output,'w')
  subprocess.Popen('lighttpd -f lighttpd.conf',stdout=log,stderr=log,shell=True).wait()

 def ssl(self):
  with open('lighttpd.conf','w') as f:f.write(lighttpd)
  subprocess.Popen("openssl req -new -x509 -keyout cert.pem \
                    -out cert.pem -days 365 -nodes -newkey rsa:2048 \
                    -subj '/C=RU'",stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def readLog(self):
  with open(self.output,'r') as f:
   for n in f:
    subprocess.call('clear',shell=True)
    print n.replace('\n','')
  os.remove(self.output)

def main():
 engine = Engine()
 engine.ssl()
 engine.kill()
 engine.lighttpdService()
 engine.lighttpdServer()
 engine.readLog()

if __name__ == '__main__':
 exit('root access required') if os.getuid() else main()
