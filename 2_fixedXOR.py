import binascii as bin
import base64

test1 = "1c0111001f010100061a024b53535009181c"
test2 = "686974207468652062756c6c277320657965"

ref = "746865206b696420646f6e277420706c6179"

#takes two hex encoded strings, xors them, then returns the corresponding string in hex
def xor(str1, str2):
    temp1 = bytearray(test1, "hex")
    temp2 = bytearray(test2, "hex")
    ret = ''
    for x in xrange(len(temp1)):
        ret += hex(int(temp1[x])^int(temp2[x])).lstrip("0x")
    return ret

def xor2(str1, str2):
    ret = ''
    for x in xrange(len(str1)):
        ret += hex(ord(str1[x])^ord(str2[x])).lstrip("0x")
    return ret

print xor(test1, test2)
print xor2(test1, test2)
#both give 75b6865265269642646546512174276c61756, which is incorrect
