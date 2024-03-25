#!/usr/bin/python

# Generates the filename based on the nickname given to the Pokemon. This file
# is now a giant mess because of the Japanese handling, but it does work.

from array import array

namelist = {
    0x21: '0',
    0x22: '1',
    0x23: '2',
    0x24: '3',
    0x25: '4',
    0x26: '5',
    0x27: '6',
    0x28: '7',
    0x29: '8',
    0x2a: '9',
    0x2b: 'A',
    0x2c: 'B',
    0x2d: 'C',
    0x2e: 'D',
    0x2f: 'E',
    0x30: 'F',
    0x31: 'G',
    0x32: 'H',
    0x33: 'I',
    0x34: 'J',
    0x35: 'K',
    0x36: 'L',
    0x37: 'M',
    0x38: 'N',
    0x39: 'O',
    0x3a: 'P',
    0x3b: 'Q',
    0x3c: 'R',
    0x3d: 'S',
    0x3e: 'T',
    0x3f: 'U',
    0x40: 'V',
    0x41: 'W',
    0x42: 'X',
    0x43: 'Y',
    0x44: 'Z',
    0x45: 'a',
    0x46: 'b',
    0x47: 'c',
    0x48: 'd',
    0x49: 'e',
    0x4a: 'f',
    0x4b: 'g',
    0x4c: 'h',
    0x4d: 'i',
    0x4e: 'j',
    0x4f: 'k',
    0x50: 'l',
    0x51: 'm',
    0x52: 'n',
    0x53: 'o',
    0x54: 'p',
    0x55: 'q',
    0x56: 'r',
    0x57: 's',
    0x58: 't',
    0x59: 'u',
    0x5a: 'v',
    0x5b: 'w',
    0x5c: 'x',
    0x5d: 'y',
    0x5e: 'z',
}

jpnamelist = {
    0x52: 'A',
    0x53: 'A',
    0x54: 'I',
    0x55: 'I',
    0x56: 'U',
    0x57: 'U',
    0x58: 'E',
    0x59: 'E',
    0x5a: 'O',
    0x5b: 'O',
    0x5c: 'KA',
    0x5d: 'GA',
    0x5e: 'KI',
    0x5f: 'GI',
    0x60: 'KU',
    0x61: 'GU',
    0x62: 'KE',
    0x63: 'GE',
    0x64: 'KO',
    0x65: 'GO',
    0x66: 'SA',
    0x67: 'ZA',
    0x68: 'SHI',
    0x69: 'JI',
    0x6a: 'SU',
    0x6b: 'ZU',
    0x6c: 'SE',
    0x6d: 'ZE',
    0x6e: 'SO',
    0x6f: 'ZO',
    0x70: 'TA',
    0x71: 'DA',
    0x72: 'CHI',
    0x73: 'JI',
    0x75: 'TSU',
    0x76: 'ZU',
    0x77: 'TE',
    0x78: 'DE',
    0x79: 'TO',
    0x7a: 'DO',
    0x7b: 'NA',
    0x7c: 'NI',
    0x7d: 'NU',
    0x7e: 'NE',
    0x7f: 'NO',
    0x80: 'HA',
    0x81: 'BA',
    0x82: 'PA',
    0x83: 'HI',
    0x84: 'BI',
    0x85: 'PI',
    0x86: 'FU',
    0x87: 'BU',
    0x88: 'PU',
    0x89: 'HE',
    0x8a: 'BE',
    0x8b: 'PE',
    0x8c: 'HO',
    0x8d: 'BO',
    0x8e: 'PO',
    0x8f: 'MA',
    0x90: 'MI',
    0x91: 'MU',
    0x92: 'ME',
    0x93: 'MO',
    0x94: 'YA',
    0x95: 'YA',
    0x96: 'YU',
    0x97: 'YU',
    0x98: 'YO',
    0x99: 'YO',
    0x9a: 'RA',
    0x9b: 'RI',
    0x9c: 'RU',
    0x9d: 'RE',
    0x9e: 'RO',
    0x9f: 'WA',
    0xa0: 'WO',
    0xa1: 'N',
    0xa2: '0',
    0xa3: '1',
    0xa4: '2',
    0xa5: '3',
    0xa6: '4',
    0xa7: '5',
    0xa8: '6',
    0xa9: '7',
    0xaa: '8',
    0xab: '9',
    0xac: 'A',
    0xad: 'B',
    0xae: 'C',
    0xaf: 'D',
    0xb0: 'E',
    0xb1: 'F',
    0xb2: 'G',
    0xb3: 'H',
    0xb4: 'I',
    0xb5: 'J',
    0xb6: 'K',
    0xb7: 'L',
    0xb8: 'M',
    0xb9: 'N',
    0xba: 'O',
    0xbb: 'P',
    0xbc: 'Q',
    0xbd: 'R',
    0xbe: 'S',
    0xbf: 'T',
    0xc0: 'U',
    0xc1: 'V',
    0xc2: 'W',
    0xc3: 'X',
    0xc4: 'Y',
    0xc5: 'Z',
    0xc6: 'a',
    0xc7: 'b',
    0xc8: 'c',
    0xc9: 'd',
    0xca: 'e',
    0xcb: 'f',
    0xcc: 'g',
    0xcd: 'h',
    0xce: 'i',
    0xcf: 'j',
    0xd0: 'k',
    0xd1: 'l',
    0xd2: 'm',
    0xd3: 'n',
    0xd4: 'o',
    0xd5: 'p',
    0xd6: 'q',
    0xd7: 'r',
    0xd8: 's',
    0xd9: 't',
    0xda: 'u',
    0xdb: 'v',
    0xdc: 'w',
    0xdd: 'x',
    0xde: 'y',
    0xdf: 'z',
    0xf1: '-'
}

ki = {
    0x44: 'KYA',
    0x46: 'KYU',
    0x48: 'KYO',
    0x94: 'KYA',
    0x96: 'KYU',
    0x98: 'KYO'
}

gi = {
    0x44: 'GYA',
    0x46: 'GYU',
    0x48: 'GYO',
    0x94: 'GYA',
    0x96: 'GYU',
    0x98: 'GYO'
}

shi = {
    0x44: 'SHA',
    0x46: 'SHU',
    0x48: 'SHO',
    0x94: 'SHA',
    0x96: 'SHU',
    0x98: 'SHO'
}

ji = {
    0x44: 'JA',
    0x46: 'JU',
    0x48: 'JO',
    0x94: 'JA',
    0x96: 'JU',
    0x98: 'JO'
}

chi = {
    0x44: 'CHA',
    0x46: 'CHU',
    0x48: 'CHO',
    0x94: 'CHA',
    0x96: 'CHU',
    0x98: 'CHO'
}

ni = {
    0x44: 'NYA',
    0x46: 'NYU',
    0x48: 'NYO',
    0x94: 'NYA',
    0x96: 'NYU',
    0x98: 'NYO'
}

hi = {
    0x44: 'HYA',
    0x46: 'HYU',
    0x48: 'HYO',
    0x94: 'HYA',
    0x96: 'HYU',
    0x98: 'HYO'
}

bi = {
    0x44: 'BYA',
    0x46: 'BYU',
    0x48: 'BYO',
    0x94: 'BYA',
    0x96: 'BYU',
    0x98: 'BYO'
}

pi = {
    0x44: 'PYA',
    0x46: 'PYU',
    0x48: 'PYO',
    0x94: 'PYA',
    0x96: 'PYU',
    0x98: 'PYO'
}

mi = {
    0x44: 'MYA',
    0x46: 'MYU',
    0x48: 'MYO',
    0x94: 'MYA',
    0x96: 'MYU',
    0x98: 'MYO'
}

ri = {
    0x44: 'RYA',
    0x46: 'RYU',
    0x48: 'RYO',
    0x94: 'RYA',
    0x96: 'RYU',
    0x98: 'RYO'
}

tsu = {
    0x5c: 'K',
    0x5d: 'G',
    0x5e: 'K',
    0x5f: 'G',
    0x60: 'K',
    0x61: 'G',
    0x62: 'K',
    0x63: 'G',
    0x64: 'K',
    0x65: 'G',
    0x66: 'S',
    0x67: 'Z',
    0x68: 'S',
    0x69: 'J',
    0x6a: 'S',
    0x6b: 'Z',
    0x6c: 'S',
    0x6d: 'Z',
    0x6e: 'S',
    0x6f: 'Z',
    0x70: 'T',
    0x71: 'D',
    0x72: 'T',
    0x73: 'D',
    0x75: 'T',
    0x76: 'D',
    0x77: 'T',
    0x78: 'D',
    0x79: 'T',
    0x7a: 'D',
    0x7b: 'N',
    0x7c: 'N',
    0x7d: 'N',
    0x7e: 'N',
    0x7f: 'N',
    0x80: 'H',
    0x81: 'B',
    0x82: 'P',
    0x83: 'H',
    0x84: 'B',
    0x85: 'P',
    0x86: 'F',
    0x87: 'B',
    0x88: 'P',
    0x89: 'H',
    0x8a: 'B',
    0x8b: 'P',
    0x8c: 'H',
    0x8d: 'B',
    0x8e: 'P',
    0x8f: 'M',
    0x90: 'M',
    0x91: 'M',
    0x92: 'M',
    0x93: 'M',
    0x9a: 'R',
    0x9b: 'R',
    0x9c: 'R',
    0x9d: 'R',
    0x9e: 'R'
}

def namegen(namebytes):
    arr = array('B')
    arr = bytearray(namebytes)
    name = ''
    skip = False
    for i in range(0, len(arr), 2):
        if arr[i] == 0xff:
            return name

        if arr[i + 1] == 0x00:  # Handling JPN names
            if skip:
                skip = False
                continue

            c = arr[i]
            n = ''
            hiragana = False

            if c < 0x52:
                c += 0x50
                hiragana = True

            # handling special cases (small ya, yu, yo, tsu)
            if c == 0x5e:
                n = ki.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'KI'
            elif c == 0x5f:
                n = gi.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'GI'
            elif c == 0x68:
                n = shi.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'SHI'
            elif c == 0x69:
                n = ji.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'JI'
            elif c == 0x72:
                n = chi.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'CHI'
            elif c == 0x7c:
                n = ni.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'NI'
            elif c == 0x83:
                n = hi.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'HI'
            elif c == 0x84:
                n = bi.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'BI'
            elif c == 0x85:
                n = pi.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'PI'
            elif c == 0x90:
                n = mi.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'MI'
            elif c == 0x9b:
                n = ri.get(arr[i + 2])
                if n:
                    skip = True
                else:
                    n = 'RI'
            elif c == 0x74:
                dbl = arr[i + 2]
                if dbl < 0x52:
                    dbl += 0x50
                n = tsu.get(dbl)
                if not n:
                    n = ''
            else:
                n = jpnamelist.get(c)
                if not n:
                    n = ''

            if hiragana:
                n = n.lower()

            name += n
        # endif arr[i + 1] == 0x00
        else:  # Non-JPN names
            try:
                name += namelist.get(arr[i])
            except:
                pass
    return name
