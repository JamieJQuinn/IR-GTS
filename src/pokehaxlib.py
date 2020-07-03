import socket, sys, time, thread

class Request:
  def __init__(self, h=None):
    if not h:
      self.action=None
      self.page=None
      self.getvars={}
      return
    if not h.startswith("GET"): raise TypeError("Not a DS header!")
    request=h[h.find("/pokemondpds/")+13:h.find("HTTP/1.1")-1]
    #request=h.split("/")[3][:h.find("HTTP")-1]
    self.page=request[:request.find("?")]
    self.action=request[request.find("/")+1:request.find(".asp?")]
    vars=dict((i[:i.find("=")],i[i.find("=")+1:]) for i in request[request.find("?")+1:].split("&"))
    self.getvars=vars
  def __str__(self):
    request="%s?%s"%(self.page, '&'.join("%s=%s"%i for i in self.getvars.items()))
    return 'GET /pokemondpds/%s HTTP/1.1\r\n'%request+ \
    'Host: gamestats2.gs.nintendowifi.net\r\nUser-Agent: GameSpyHTTP/1.0\r\n'+ \
    'Connection: close\r\n\r\n'
  def __repr__(self):
    return "<Request for %s, with %s>"%(self.action, ", ".join(i+"="+j for i, j in self.getvars.items()))

class Response:
  pokes=None
  resps=None
  def __init__(self, h):
    if not h.startswith("HTTP/1.1"):
      self.data=h
      return
    h=h.split("\r\n")
    while True:
      line=h.pop(0)
      if not line: break
      elif line.startswith("P3P"): self.p3p=line[line.find(": ")+2:] #I don't know what this is
      elif line.startswith("cluster-server"): self.server=line[line.find(": ")+2:] #for fun
      elif line.startswith("X-Server-"): self.sname=line[line.find(": ")+2:] #for fun
      elif line.startswith("Content-Length"): self.len=int(line[line.find(": ")+2:]) #need
      elif line.startswith("Set-Cookie"): self.cookie=line[line.find(": ")+2:] #don't need
    self.data="\r\n".join(h)

  def __str__(self):
    months=["???", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
            "Aug", "Sep", "Oct", "Nov", "Dec"]
    days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    t=time.gmtime()
    return "HTTP/1.1 200 OK\r\n"+ \
           "Date: %s, %02i %s %i %02i:%02i:%02i GMT\r\n"%(days[t[6]],
                     t[2], months[t[1]], t[0], t[3], t[4], t[5]) + \
           "Server: Microsoft-IIS/6.0\r\n"+ \
           "P3P: CP='NOI ADMa OUR STP'\r\n"+ \
           "cluster-server: aphexweb3\r\n"+ \
           "X-Server-Name: AW4\r\n"+ \
           "X-Powered-By: ASP.NET\r\n"+ \
           "Content-Length: %i\r\n"%len(self.data)+ \
           "Content-Type: text/html\r\n"+ \
           "Set-Cookie: ASPSESSIONIDQCDBDDQS=JFDOAMPAGACBDMLNLFBCCNCI; path=/\r\n"+ \
           "Cache-control: private\r\n\r\n"+self.data

  def getpkm(self):
    all=[]
    data=self.data
    while data:
      result=data[:292]; data=data[292:]
      all.append(result[:136])
    return all

def dnsspoof():
  s=socket.socket(); s.connect(("4.2.2.2",53));
  me="".join(chr(int(x)) for x in s.getsockname()[0].split("."))
  print "Please set your DS's DNS server to",s.getsockname()[0]
  dnsserv=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  dnsserv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  dnsserv.bind(("0.0.0.0",53))
  while True:
    r=dnsserv.recvfrom(512)
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('4.2.2.2', 53))
    s.send(r[0])
    rr=s.recv(512)
    if "gamestats2" in rr: rr=rr[:-4]+me
    dnsserv.sendto(rr, r[1])

serv=None
log=None
def initServ(logfile=None):
  global serv, log
  thread.start_new_thread(dnsspoof,())
  serv=socket.socket()
  serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  serv.bind(("0.0.0.0",80))
  serv.listen(5)

  if logfile: log=open(logfile, 'w')

def getReq():
  global serv, log
  sock, addr = serv.accept()
  sock.settimeout(2)
  data=""
  while True:
    try:
      a=sock.recv(500)
      data+=a
    except socket.timeout:
      break
  ans=Request(data)
  if log: log.write(data+"\ndone---done\n")
  #print addr, " requested ",  repr(ans)
  return sock, ans

def sendResp(sock, data):
  global serv, log
  resp=Response(data) if not isinstance(data, Response) else data
  if log: log.write(str(resp)+"\ndone---done\n")
  return sock.send(str(resp))

def respFromServ(req):
  s=socket.socket()
  #s.connect(("gamestats2.gs.nintendowifi.net", 80))
  s.connect(("207.38.11.146", 80))
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
