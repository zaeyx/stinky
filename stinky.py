#/usr/bin/python
#Stinky
#Development Ver 1 (POC)

from scapy.all import Raw, rdpcap, send
import ConfigParser
import random
from random import choice
import hashlib
import time
import socket
import sys
import BaseHTTPServer
import subprocess
from SimpleHTTPServer import SimpleHTTPRequestHandler

def Config(section):
	Conf = ConfigParser.ConfigParser()
	Conf.read('./stinky.conf')
	drawer = {}
	options = Conf.options(section)
	for option in options:
		try:
			drawer[option] = Conf.get(section, option)
			if drawer[option]== -1:
				DebugPrint("Skip: %s" % option)
		except:
			print("Exception %s" % option)
			drawer[option] = None
	return drawer

class Handle(BaseHTTPServer.BaseHTTPRequestHandler):
	#list = ['admin','IT','James','Gandalf','toor','karl','janice']
	#def passwd():
	#	num = random.random(10000,900000)
	#	h = hashlib.md5()
	#	h.update(num)
	#	return h.hexdigest()

	def do_GET(self):
		audit_path = str.split(self.path, "?")
		if self.path != "/" and audit_path[0] != "/login.php" and self.path != "/favicon.ico":
			self.send_error(404, "file not found")
			return
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.end_headers()
		try:
			stdout = sys.stdout
			sys.stdout = self.wfile
			self.makepage()
		finally:
			sys.stdout = stdout

	def makepage(self):
		if self.path == "/":
			f = open("./index.html","r")
		elif self.path == "/favicon.ico":
			f = open("./favicon.ico","r")
		else:
			write = True
			whitelist = str.split(Config("WebServ")["whitelist"],',')
			#t = str.split(self.path,"pass")
			#t = str.split(t[1],"&")
			#if t[0] == "=asdf":
			for ip in whitelist:
				if self.address_string() == ip:
					write = False
					break
			if write == True:
				alert_string = self.address_string() + ":" + self.path + "\n"
				alert = open("./log.stinky","a")
				alert.write(alert_string)
				alert.close()
			
			f = open("./login.html","r")
		#Main Page Writing flow
		rep = f.read()
		f.close()
		self.wfile.write(rep)
		list = str.split(Config("WebServ")['list'],',')
		for i in list:
			chance = random.randint(1,4)
			if chance == 4:
				print "REMOVE AFTER DEBUG <br />"
				num = random.randint(90000,9000000)
				h = hashlib.md5()
				h.update(str(num))
				print "<br />" + i + ":" + h.hexdigest()
		

def WebServ(port):
	#HandlerClass = SimpleHTTPRequestHandler
	ServerClass  = BaseHTTPServer.HTTPServer
	Protocol	 = "HTTP/1.1"


	if port == '':
		port = 8080
	else:
		port = int(port)
	server_address = ('0.0.0.0', port)

	#HandlerClass.protocol_version = Protocol
	httpd = ServerClass (server_address, Handle)

	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa [1], "..."
	#print urlparse.parse_qs(os.environ['QUERY_STRING'])
	httpd.serve_forever()

def Login(page, HOST, PORT):
		if PORT == '':
			PORT = 8080
		if HOST == '':
			HOST = '127.0.0.1'

		passwdfile = Config("HoneyPackets")['passwdfile']
		fi = open(passwdfile,'r')
		passwdlist = str.split(fi.read(), ',')
		fi.close()
		passwd = choice(passwdlist)

		userfile = Config("WebServ")['userfile']
		fi = open(userfile,'r')
		userlist = str.split(fi.read(),',')
		fi.close()
		username = choice(userlist)

		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		s.connect(( HOST, int(PORT) ))
		#message = "GET /index.html HTTP/1.0"
		#s.sendall(message)
		#data = s.recv(2048)
		message = "GET /login.html?user=" + username + "&pass=" + passwd + "&submit=Login&page=Admin.php?screen=" + str(page) + ".cgi" #\nReferrer: www.google.com \nUser-Agent: TinyBrowse1.3"
		#message = "GET /login.php?user=" + username + "&pass=" + passwd + "&submit=Login HTTP/1.1 \nHost: 127.0.0.1 \nConnection: keep-alive \nUser-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 \nAccept-Encoding: gzip,deflate,sdch \nAccept-Language: en-US,en;q=0.8 \nAccept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3 \n"
		#^^Long string I know, I need to edit this a ton
		#Note... The size of this string is related to the broken pipe
		s.sendall(message)
		#data2 = s.recv(20)
		s.close()

def Jam():
	#lol @ def jam
	#a = rdpcap('./net.pcap')
	a = Raw("Do I really smell this good?")
	while True:
		send(a)
		#uncomment the below for a good time
		#way more effective... 
		#hold ctrl + c to eject and don't end up like goose.
		#send(a,0,100)

print "1) Web Server HoneyLogin"
print "2) Network Traffic HoneyPackets"
print "3) Sniffer Jammer"

sel = raw_input("Select Mode 1-3: ")
if int(sel) == 1:
	port = raw_input("Enter the port to listen on(8080): ")
	WebServ(port)
elif int(sel) == 2:
	HOST = raw_input("Enter IP to connect to(127.0.0.1): ")
	PORT = raw_input("Enter Port(8080): ")
	while True:
		f = random.randint(1, 10)
		Login(f, HOST, PORT)
		rand = random.randint(20, 45)
		time.sleep(rand)
elif int(sel) == 3:
	Jam()

else:
	print "Nothing else created"
