test1 = "1c0111001f010100061a024b53535009181c"
test2 = "686974207468652062756c6c277320657965"

ref = "746865206b696420646f6e277420706c6179"

#takes two hex encoded strings, xors them, then returns the corresponding string in hex
def xor(str1, str2):
    if len(str1)!=len(str2):
        raise Exception("length differential in xor")
    ret = ''
    for x in xrange(len(str1)):
        ret += hex(int(str1[x],16)^int(str2[x],16))[2:]#takes out the 0x
    return ret


#print xor(test1, test2)
#print xor(test1, test2) == ref
