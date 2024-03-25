from __future__ import print_function
import socket, sys, time, threading

class Request:
  def __init__(self, h=None):
    if not h:
      self.action=None
      self.page=None
      self.getvars={}
      return
    if not h.startswith(b"GET"): raise TypeError("Not a DS header!")
    request=h[h.find(b"/pokemondpds/")+13:h.find(b"HTTP/1.1")-1]
    #request=h.split("/")[3][:h.find("HTTP")-1]
    self.page=request[:request.find(b"?")]
    self.action=request[request.find(b"/")+1:request.find(b".asp?")]
    vars=dict((i[:i.find(b"=")],i[i.find(b"=")+1:]) for i in request[request.find(b"?")+1:].split(b"&"))
    self.getvars=vars
  def __str__(self):
    request="%s?%s"%(self.page, '&'.join("%s=%s"%i for i in self.getvars.items()))
    return b'GET /pokemondpds/%s HTTP/1.1\r\n'%request+ \
    b'Host: gamestats2.gs.nintendowifi.net\r\nUser-Agent: GameSpyHTTP/1.0\r\n'+ \
    b'Connection: close\r\n\r\n'
  def __repr__(self):
    return b"<Request for %s, with %s>"%(self.action, ", ".join(i+"="+j for i, j in self.getvars.items()))

class Response:
  pokes=None
  resps=None
  def __init__(self, h):
    if not h.startswith(b"HTTP/1.1"):
      self.data=h
      return
    h=h.split("\r\n")
    while True:
      line=h.pop(0)
      if not line: break
      elif line.startswith(b"P3P"): self.p3p=line[line.find(": ")+2:] #I don't know what this is
      elif line.startswith(b"cluster-server"): self.server=line[line.find(": ")+2:] #for fun
      elif line.startswith(b"X-Server-"): self.sname=line[line.find(": ")+2:] #for fun
      elif line.startswith(b"Content-Length"): self.len=int(line[line.find(": ")+2:]) #need
      elif line.startswith(b"Set-Cookie"): self.cookie=line[line.find(": ")+2:] #don't need
    self.data="\r\n".join(h)

  def ret(self):
    months=[b"???", b"Jan", b"Feb", b"Mar", b"Apr", b"May", b"Jun", b"Jul",
            b"Aug", b"Sep", b"Oct", b"Nov", b"Dec"]
    days=[b"Mon", b"Tue", b"Wed", b"Thu", b"Fri", b"Sat", b"Sun"]
    t=time.gmtime()
    return b"HTTP/1.1 200 OK\r\n"+ \
           b"Date: %s, %02i %s %i %02i:%02i:%02i GMT\r\n"%(days[t[6]],
                     t[2], months[t[1]], t[0], t[3], t[4], t[5]) + \
           b"Server: Microsoft-IIS/6.0\r\n"+ \
           b"P3P: CP='NOI ADMa OUR STP'\r\n"+ \
           b"cluster-server: aphexweb3\r\n"+ \
           b"X-Server-Name: AW4\r\n"+ \
           b"X-Powered-By: ASP.NET\r\n"+ \
           b"Content-Length: %i\r\n"%len(self.data)+ \
           b"Content-Type: text/html\r\n"+ \
           b"Set-Cookie: ASPSESSIONIDQCDBDDQS=JFDOAMPAGACBDMLNLFBCCNCI; path=/\r\n"+ \
           b"Cache-control: private\r\n\r\n"+self.data

  def getpkm(self):
    all=[]
    data=self.data
    while data:
      result=data[:292]; data=data[292:]
      all.append(result[:136])
    return all

def dnsspoof():
  dns_server = "178.62.43.212" # This is the unofficial pkmnclassic.net server
  s=socket.socket()
  s.connect((dns_server,53))
  me=b"".join(bytes([int(x)]) for x in s.getsockname()[0].split("."))
  print(me)
  print("Please set your DS's DNS server to",s.getsockname()[0])
  dnsserv=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  dnsserv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  dnsserv.bind(("0.0.0.0",53))
  while True:
    r=dnsserv.recvfrom(512)
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((dns_server, 53))
    s.send(r[0])
    rr=s.recv(512)
    print(type(rr))
    print('before: ', rr)
    if "gamestats2" in str(rr): rr=rr[:-4]+me
    print('after: ', rr)
    print('---')
    dnsserv.sendto(rr, r[1])

serv=None
log=None
def initServ(logfile=None):
  global serv, log
  threading._start_new_thread(dnsspoof,())
  serv=socket.socket()
  serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  serv.bind(("0.0.0.0",80))
  serv.listen(5)

  if logfile: log=open(logfile, 'w')

def getReq():
  global serv, log
  sock, addr = serv.accept()
  sock.settimeout(2)
  data=b""
  while True:
    try:
      a=sock.recv(500)
      data+=a
    except socket.timeout:
      break
  ans=Request(data)
  if log: log.write(data+"\ndone---done\n")
  # print addr, " requested ",  repr(ans)
  return sock, ans

def sendResp(sock, data):
  global serv, log
  resp=Response(data) if not isinstance(data, Response) else data
  if log: log.write(str(resp)+"\ndone---done\n")
  print(resp.ret())
  return sock.send(resp.ret())

def respFromServ(req):
  s=socket.socket()
  #s.connect(("gamestats2.gs.nintendowifi.net", 80))
  # s.connect(("207.38.11.146", 80))
  s.connect(("178.62.43.212", 80))
  s.send(str(req))
  data=""
  while True:
    a=s.recv(500)
    if not a: break
    data+=a
  return Response(data)

def serverResp():
  sock, req=getReq()
  resp=respFromServ(req)
  sendResp(sock, resp)
