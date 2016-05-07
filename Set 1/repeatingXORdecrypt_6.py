import binascii, base64
from operator import itemgetter
import singlebyteXOR_3 as xor

#takes two ascii strings
def HammingDistance(str1, str2):
    if len(str1)!=len(str2):
        raise Exception("Differing string lengths")
    arr1 = bytearray(binascii.hexlify(str1).decode("hex"))
    arr2 = bytearray(binascii.hexlify(str2).decode("hex"))
    count = 0
    for i in xrange(len(arr1)):
        bin1 = bin(arr1[i])[2:].zfill(8)
        bin2 = bin(arr2[i])[2:].zfill(8)
        for j in xrange(8):
            if bin1[j]!=bin2[j]:
                count += 1
    return count

#takes two bytearrrays
def HammingB(arr1, arr2):
    if len(arr1)!=len(arr2):
        raise Exception("Differing array lengths")
    count = 0
    for i in xrange(len(arr1)):
        bin1 = bin(arr1[i])[2:].zfill(8)
        bin2 = bin(arr2[i])[2:].zfill(8)
        for j in xrange(8):
            if bin1[j]!=bin2[j]:
                count += 1
    return count

#takes hex string
#returns N best possiblities
def findNkeysizes(str1,N):
    arr = bytearray(str1.decode("hex"))
    distances = []
    
    for size in xrange(2,40):
        try:
            arr1 = arr[:size]
            arr2 = arr[size:2*size]
            arr3 = arr[2*size:3*size]
            arr4 = arr[3*size:4*size]
        except:
            print "index out of bounds - key is too long for the message"
        #average the normalized hamming distances btw 4 blocks of guessed key size
        count = HammingB(arr1,arr2)+HammingB(arr1,arr3)+HammingB(arr1,arr4)
        count += HammingB(arr2,arr3)+HammingB(arr2,arr4)+HammingB(arr3,arr4)
        distances.append([size,float(count)/size])
    distances.sort(key = itemgetter(1))
    return [item[0] for item in distances[:N]]

#takes ascii string, ascii key
#returns hex string
def encode_repeating_xor(str1,key):
    #convert both to arrays of hex values
    array = bytearray(binascii.hexlify(str1).decode("hex"))
    bytearr = bytearray(binascii.hexlify(key).decode("hex"))   
    for i in xrange(len(array)):
        array[i] ^= bytearr[i%(len(key))]
    return binascii.hexlify(str(array))

#takes hex string, integer size
#returns key as a hex string
def breaktext(str1,size):
    #breaks text, then solves each break as a single character xor
    substrings = [str1[i:i+2] for i in range(0, len(str1), 2)]
    blocks = [substrings[i::size] for i in range(size)]
    blocks = ["".join(block) for block in blocks]
    try:
        key = [xor.printNtranslations(block,1)[0][1][2:].zfill(2) for block in blocks]
    except:
        return
    return "0x"+"".join(key)

#takes hex string, hex key
#returns hex string
def encode_helper(str1,key):
    #convert both to arrays of hex values
    if key[:2] == "0x":
        key = key[2:]
    textarr = bytearray(str1.decode("hex"))
    keyarr = bytearray(key.decode("hex"))
    print textarr[0],keyarr[0]
    for i in xrange(len(textarr)):
        textarr[i] ^= keyarr[i%len(keyarr)]
    return binascii.hexlify(textarr)

#takes text to break, number of possible decryptions to return
def break_cipher(str1, N):
    sizes = findNkeysizes(str1, N)
    keys = [breaktext(str1, size) for size in sizes]
    keys = [key for key in keys if key!=None]
    encodings = [encode_helper(str1,key) for key in keys]
    return zip(*[encodings, keys])

#return [ascii decrypted text, hex key]
def best_guess(str1):
    vals = break_cipher(str1,1)[0]
    return [binascii.unhexlify(vals[0]), vals[1]]#return key for ascii key

#file = open("challenge6.txt","r").read()
#text = "".join([line for line in file.splitlines()])
#text = binascii.hexlify(base64.b64decode(text))
#print best_guess(text)[0]
