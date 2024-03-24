#!/usr/bin/python

from __future__ import print_function
from __future__ import absolute_import
from .pokehaxlib import *
from .pkmlib import encode
from .boxtoparty import makeparty
from .gbatonds import makends
from sys import argv, exit
from platform import system
import os.path

def sendpkm():
    token = b'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'

    print('Note: you must exit the GTS before sending a pkm')
    print('Enter the path or drag the pkm file here')

    path = input().strip()
    path = os.path.normpath(path)
    if system() != 'Windows':
        path = path.replace('\\', '')

    if path.lower().endswith('.pkm'):
        with open(path, 'rb') as f:
            pkm = f.read()

        # Adding extra 100 bytes of party data
        if len(pkm) != 236 and len(pkm) != 136:
            print('Invalid filesize.')
            return
        if len(pkm) == 136:
            print('PC-Boxed Pokemon! Adding party data...', end=' ')
            pkm = makeparty(pkm)
            print('done.')

        print('Encoding!')
        bin = encode(pkm)
    elif path.lower().endswith('.3gpkm'):
        print('Converting GBA file to NDS format...', end=' ')
        with open(path, 'rb') as f:
            pkm = f.read()

        if len(pkm) != 80 and len(pkm) != 100:
            print('Invalid filesize.')
            return
        pkm = makends(pkm)
        print('done.')

        print('Encoding!')
        bin = encode(pkm)
    else:
        print('Filename must end in .pkm or .3gpkm')
        return

    # Adding GTS data to end of file
    bin += pkm[0x08:0x0a] # id
    if ord(bytes([pkm[0x40]])) & 0x04: bin += b'\x03' # Gender
    else: bin += bytes([((ord(bytes([pkm[0x40]])) & 2) + 1)])
    bin += bytes([pkm[0x8c]]) # Level
    bin += b'\x01\x00\x03\x00\x00\x00\x00\x00' # Requesting bulba, either, any
    bin += b'\x00' * 20 # Timestamps and PID
    bin += pkm[0x68:0x78] # OT Name
    bin += pkm[0x0c:0x0e] # OT ID
    bin += b'\xDB\x02' # Country, City
    bin += b'\x46\x00\x07\x02' # Sprite, Exchanged (?), Version, Lang

    sent = False
    delete = False
    print('Ready to send; you can now enter the GTS...')
    while not sent:
        sock, req = getReq()
        a = req.action
        if len(req.getvars) == 1:
            sendResp(sock, token)
        elif a == b'info':
            sendResp(sock, b'\x01\x00')
            print('Connection Established.')
        elif a == b'setProfile': sendResp(sock, b'\x00' * 8)
        elif a == b'post': sendResp(sock, b'\x0c\x00')
        elif a == b'search': sendResp(sock, b'')
        elif a == b'result': sendResp(sock, bin)
        elif a == b'delete':
            sendResp(sock, b'\x01\x00')
            sent = True

    print('Pokemon sent successfully.', end=' ')
