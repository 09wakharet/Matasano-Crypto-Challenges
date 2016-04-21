from fixedXOR_2 import xor
import binascii

print xor("abc","b23")

test = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

#str1 is a hex string, byte1 a hex byte
def xor_byte(str1, byte1):
    ret = ''
    byte = byte1
    for x in xrange(len(str1)):
        ret += hex(int(str1[x],16)^int(byte,16))[2:]#takes out the 0x
    return ret

def hextoascii(str1):
    temp = binascii.unhexlify(str1)
    return binascii.b2a_qp(temp)

print xor_byte(test, "a")
print hextoascii("2d54")
