import itertools, struct
shiftind='\x00\x01\x02\x03\x00\x01\x03\x02\x00\x02\x01\x03\x00\x02\x03\x01\x00\x03\x01\x02\x00\x03\x02\x01\x01\x00\x02\x03\x01\x00\x03\x02\x01\x02\x00\x03\x01\x02\x03\x00\x01\x03\x00\x02\x01\x03\x02\x00\x02\x00\x01\x03\x02\x00\x03\x01\x02\x01\x00\x03\x02\x01\x03\x00\x02\x03\x00\x01\x02\x03\x01\x00\x03\x00\x01\x02\x03\x00\x02\x01\x03\x01\x00\x02\x03\x01\x02\x00\x03\x02\x00\x01\x03\x02\x01\x00'

class pokemon:
  pass

class makerand:
  def __init__(self, rngseed):
    self.rngseed=rngseed
  def rand(self):
    self.rngseed=0x41C64E6D * self.rngseed + 0x6073
    self.rngseed&=0xFFFFFFFF
    return self.rngseed>>16
  __call__=rand
  

def encode(pkm):
  s=list(struct.unpack("IHH"+"H"*(len(pkm)/2-4), pkm))
  shift=((s[0]>>0xD & 0x1F) %24)
  order=[ord(i) for i in shiftind[4*shift:4*shift+4]]
  shifted=s[:3]
  for i in order: shifted+=s[3+16*i:19+16*i]
  shifted+=s[67:]

  rand=makerand(s[2])
  for i in range(3, 67): shifted[i]^=rand()
  if len(shifted)>67:
    rand=makerand(shifted[0])
    for i in range(67, len(shifted)): shifted[i]^=rand()
  return struct.pack("IHH"+"H"*(len(pkm)/2-4), *shifted)
  
def decode(bin):
  shifted=list(struct.unpack("IHH"+"H"*(len(bin)/2-4), bin))
  rand=makerand(shifted[2])
  for i in range(3, 67): shifted[i]^=rand()
  if len(shifted)>67:
    rand=makerand(shifted[0])
    for i in range(67, len(shifted)): shifted[i]^=rand()
  
  shift=((shifted[0]>>0xD & 0x1F) %24)
  order=[ord(i) for i in shiftind[4*shift:4*shift+4]]
  s=shifted[:3]
  for i in range(4): s+=shifted[3+16*order.index(i):19+16*order.index(i)]
  s+=shifted[67:]
  return struct.pack("IHH"+"H"*(len(bin)/2-4), *s)
