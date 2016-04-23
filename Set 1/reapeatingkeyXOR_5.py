import binascii, base64

test = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
key = "ICE"

#takes ascii string, ascii key
def xor_key(str1, key):
    #convert both to arrays of hex values
    array = bytearray(binascii.hexlify(str1).decode("hex"))
    bytearr = bytearray(binascii.hexlify(key).decode("hex"))   
    for i in xrange(len(array)):
        array[i] ^= bytearr[i%(len(key))]
    return binascii.hexlify(str(array))

print xor_key(test,key)

#SHOULD RETURN:
#0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
#a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
