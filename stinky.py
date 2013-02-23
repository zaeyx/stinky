#/usr/bin/python
#Stinky
#Development Ver 1 (POC)

from scapy.all import rdpcap, send
import random
import time
import socket
import sys
import BaseHTTPServer
import subprocess
from SimpleHTTPServer import SimpleHTTPRequestHandler

def WebServ():
	HandlerClass = SimpleHTTPRequestHandler
	ServerClass  = BaseHTTPServer.HTTPServer
	Protocol	 = "HTTP/1.0"

	if sys.argv[1:]:
		port = int(sys.argv[1])
	else:
		port = 8080
	server_address = ('0.0.0.0', port)

	HandlerClass.protocol_version = Protocol
	httpd = ServerClass (server_address, HandlerClass)

	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa [1], "..."
	#print urlparse.parse_qs(os.environ['QUERY_STRING'])
	httpd.serve_forever()

def Login(page, HOST):
		PORT = 8080
		if HOST == '':
			HOST = '127.0.0.1'
		
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		s.connect(( HOST, PORT ))
		message = "GET /index.html HTTP/1.0"
		s.sendall(message)
		#data = s.recv(2048)
		message = "GET /login.html?user=administrator&pass=password123!&submit=Login&page=Admin.php?screen=" + str(page) + ".cgi \n Referrer: www.google.com \n User-Agent: TinyBrowse1.3"
		s.sendall(message)
		#data2 = s.recv(2048)
		s.close()

def Jam():
	a = rdpcap('./net.pcap')
	while True:
		send(a)

print "1) Web Server HoneyLogin"
print "2) Network Traffic HoneyPackets"
print "3) Sniffer Jammer"

sel = raw_input("Select Mode 1-3: ")
if int(sel) == 1:
	WebServ()
elif int(sel) == 2:
	HOST = raw_input("Enter IP to connect to(127.0.0.1): ")
	while True:
		f = random.randint(1, 10)
		Login(f, HOST)
		rand = random.randint(20, 45)
		time.sleep(rand)
elif int(sel) == 3:
	Jam()

else:
	print "Nothing else created"
