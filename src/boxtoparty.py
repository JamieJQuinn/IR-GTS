# An attempt to fix the problem of uploading 136-byte ('boxed') Pokemon to
# the DS. This should properly generate the battle stats so it can be read
# by the games.

from __future__ import division
from array import array
from src.pokemon import PokemonData

pkm = None

def ivcheck(b):
    ivs = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
    hp =  (ivs & 0x0000001f)
    atk = (ivs & 0x000003e0) >> 5
    df =  (ivs & 0x00007c00) >> 10
    spe = (ivs & 0x000f8000) >> 15
    spa = (ivs & 0x01f00000) >> 20
    spd = (ivs & 0x3e000000) >> 25
    return (hp, atk, df, spa, spd, spe)

def evcheck(b):
    hp = b[0]
    atk = b[1]
    df = b[2]
    spe = b[3]
    spa = b[4]
    spd = b[5]
    total = hp + atk + df + spe + spa + spd
    return (hp, atk, df, spa, spd, spe, total)

def add_battle_stats(p):
    global pkm
    pkm = array('B')
    pkm.fromstring(p)

    lv = __level()
    id = pkm[0x08] + (pkm[0x09] << 8)

    s = ''
    s += '\x00' * 4      # 0x88 to 0x8b
    s += chr(lv)         # 0x8c
    s += '\x00'          # 0x8d
    s += __stats(lv, id) # 0x8e to 0x9b
    s += '\x00' * 5      # 0x9c to 0xa0
    s += '\x02'          # 0xa1
    s += '\x07'          # 0xa2
    s += '\xff' * 23     # 0xa3 to 0xb9
    s += '\x00' * 2      # 0xba to 0xbb
    s += '\xff' * 2      # 0xbc to 0xbd
    if pkm[0x40] & 4:    # 0xbe to 0xbf; de01 if genderless, 0000 otherwise
        s += '\xde\x01'
    else:
        s += '\x00\x00'
    s += '\xff' * 7      # 0xc0 to 0xc6
    s += '\x88'          # 0xc7
    s += '\x01'          # 0xc8
    s += '\xff' * 5      # 0xc9 to 0xcd
    s += '\xac'          # 0xce
    s += '\x01'          # 0xcf
    s += '\xff' * 4      # 0xd0 to 0xd3
    s += '\x00' * 23     # 0xd4 to 0xea
    s += '\x07'          # 0xeb

    return p + s

def __level():
    exp = pkm[0x10] + (pkm[0x11] << 8) + (pkm[0x12] << 16)
    id = pkm[0x08] + (pkm[0x09] << 8)
    exptype = PokemonData().base_stats[id][0]
    for i in range(100):
        xpneeded = PokemonData().level_curves[i + 1][exptype]
        if xpneeded > exp:
            return i
    return 100

def __stats(level, species):
    base = PokemonData().base_stats[species][1:]
    ivs = ivcheck(pkm[0x38:0x3c])
    evs = evcheck(pkm[0x18:0x1e])[:-1]

    pid = pkm[0] + (pkm[1] << 8) + (pkm[2] << 16) + (pkm[3] << 24)
    nat = PokemonData().nature_modifiers[pid % 25]

    hp = int((((ivs[0] + (2 * base[0]) + (evs[0] / 4) + 100) * level) / 100) \
            + 10)
    hpa = chr(hp >> 8)
    hpb = chr(hp & 0xff)

    atk = __genstat(ivs[1], evs[1], base[1], level, nat[0])
    df = __genstat(ivs[2], evs[2], base[2], level, nat[1])
    spe = __genstat(ivs[5], evs[5], base[5], level, nat[2])
    spa = __genstat(ivs[3], evs[3], base[3], level, nat[3])
    spd = __genstat(ivs[4], evs[4], base[4], level, nat[4])

    # Max HP, Curr HP, followed by remainder of the stats
    return hpb + hpa + hpb + hpa + atk + df + spe + spa + spd

def __genstat(iv, ev, base, level, nat):
    st = int((((iv + (2 * base) + (ev / 4)) * level) / 100) + 5)
    st = int(st * nat)

    sta = chr(st >> 8)
    stb = chr(st & 0xff)
    return stb + sta

