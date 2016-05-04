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

#takes text to break, number of possible decryptions to return
def break_cipher(str1, N):
    sizes = findNkeysizes(str1, N)
    keys = [breaktext(str1, size) for size in sizes]
    keys = [key for key in keys if key!=None]
    encodings = [encode_repeating_xor(str1,key) for key in keys]
    return zip(*[encodings, keys])

#return [ascii decrypted text, hex key]
def best_guess(str1):
    vals = break_cipher(str1,1)[0]
    key = bytearray(vals[1][2:].decode("hex"))
    text = bytearray(vals[0][2:].decode("hex"))
    for i in xrange(len(text)):
        text[i] ^= key[i%(len(vals[1])/2-1)]
    return [str(text), vals[1]]

file = open("challenge6.txt","r").read()
text = "".join([line for line in file.splitlines()])
text = binascii.hexlify(base64.b64decode(text))
print binascii.unhexlify(best_guess(text)[1][2:])

#problem_string = "4e07644e1a0f14004e4e1a1d1701074e490d4e190b0a4e4e640c1b010b4e0227000f3d3a1c1c000d1c024e1e0f6427640217001e4e2d001a0614070707000a491c1a1a4e4e08371d0b0b011a0a1c640b4e061742091d1a1d170a171d06063e0b4e0305"
#print chr(int(xor.printNtranslations(test2,2)[1][1],16))
#TODO print decrypted file
