#!/usr/bin/python

# A simple script to copy pokemon from retail carts to a computer via GTS.
# Heavily relies on the sendpkm script and the description of the GTS protocol
# from http://projectpokemon.org/wiki/GTS_protocol
#
# --Infinite Recursion

from __future__ import print_function
from __future__ import absolute_import
from .pokehaxlib import *
from .pkmlib import decode
from sys import argv, exit
from random import sample
from time import sleep
from base64 import b64decode
from binascii import hexlify
from array import array
from .namegen import namegen
from .stats import statread
from os import mkdir
import os.path, subprocess, platform

def makepkm(bytes):
    ar = array('B') # Byte array to hold encrypted data
    #ar.fromstring(bytes)
    ar = bytearray(bytes)

    # checksum is first four bytes of data, xor'd with 0x4a3b2c1d
    chksm = (eval(b'0x' + hexlify(ar[0:4]))) ^ 0x4a3b2c1d

    bin = ar[4:len(ar)] # Byte array for decrypt operations
    pkm = array('B')    # ...and one for the output file

    # Running decryption algorithm
    GRNG = chksm | (chksm << 16)
    for i in range(len(bin)):
        GRNG = (GRNG * 0x45 + 0x1111) & 0x7fffffff
        keybyte = (GRNG >> 16) & 0xff
        pkm.append((bin[i] ^ keybyte) & 0xff)

    pkm = pkm[4:len(pkm)]
    pkm = pkm[0:236].tobytes()
    pkm = decode(pkm)

    return pkm

def save(path, data):
    saved = False
    if not os.path.isdir('Pokemon'):
        mkdir('Pokemon')

    while not saved:
        fullpath = os.path.normpath('Pokemon' + os.sep + path)
        saved = True
        if os.path.isfile(fullpath):
            print('%s already exists! Delete?' % path)
            response = input().lower()
            if response != 'y' and response != 'yes':
                print('Enter new filename: (press enter to cancel save) ')
                path = input()
                if path == '':
                    print('Not saved.', end=' ')
                    return
                if not path.strip().lower().endswith('.pkm'):
                    path += '.pkm'
                saved = False

    with open(fullpath, 'wb') as f:
        f.write(data)

    print('%s saved successfully.' % path, end=' ')

def getpkm():
    token = b'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'
    sent = False
    print('Ready to receive from NDS')
    while not sent:
        sock, req = getReq()
        a = req.action

        print(a)
        if len(req.getvars) == 1: sendResp(sock, token)
        elif a == b'info':
            sendResp(sock, b'\x01\x00')
            print('Connection Established.')
        elif a == b'setProfile': sendResp(sock, b'\x00' * 8)
        elif a == b'result': sendResp(sock, b'\x05\x00')
        elif a == b'delete': sendResp(sock, b'\x01\x00')
        elif a == b'search': sendResp(sock, b'')
        elif a == b'post':
            sendResp(sock, b'\x0c\x00')
            print('Receiving Pokemon...')
            data = req.getvars[b'data']
            bytes = b64decode(data.replace(b'-', b'+').replace(b'_', b'/'))
            decrypt = makepkm(bytes)
            filename = namegen(decrypt[0x48:0x5e])
            filename += '.pkm'
            save(filename, decrypt)
            statread(decrypt)
            sent = True
