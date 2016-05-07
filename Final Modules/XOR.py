import binascii, base64, string
import collections
from operator import itemgetter


#takes ascii string, ascii key
def xor_key(str1, key):
    #convert both to arrays of hex values
    array = bytearray(binascii.hexlify(str1).decode("hex"))
    bytearr = bytearray(binascii.hexlify(key).decode("hex"))   
    for i in xrange(len(array)):
        array[i] ^= bytearr[i%(len(key))]
    return binascii.hexlify(str(array))

#str1 is a hex string, byte a hex byte
#returns a valid ascii string
#throws away strings with non-ascii characters (returns none)
def xor_byte(str1, byte):
    hex_data = str1.decode("hex")
    array = bytearray(hex_data)
    for i in xrange(len(array)):
        array[i] ^= int(byte,16)
        if chr(array[i]) not in string.printable:
            return
    return str(array)

#returns chi square based frequency analysis
#modified to penalize non text characters
def chi2_score(str1):
    english_freq = {'a':0.08167,'b':0.01492, 'c':0.02782, 'd':0.04253,
                    'e':0.12702, 'f':0.02228, 'g':0.02015, 'h':0.06094,
                    'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025,
                    'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929,
                    'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056,
                    'u':0.02758, 'v':0.00978, 'w':0.02360, 'x':0.00150,
                    'y':0.01974, 'z':0.00074}#frequencies of a-z
    frequencies =  collections.Counter(str1.lower())
    chi2 = 0.
    ignored = 0.
    for k in frequencies:
        if k not in string.ascii_letters:
            ignored+=frequencies[k]
            continue
        obs = float(frequencies[k])
        exp = float(english_freq[k]*len(str1))
        chi2 += float(pow(obs-exp,2)/exp)
    if ignored/len(str1) > .5:
        return 100000
    return chi2 + 2*ignored

def dict_scores(str1):
    ciphers = []
    for i in xrange(256):
        temp = xor_byte(str1,hex(i))
        if temp is not None:
            ciphers.append(temp)
    scored_ciphers = []
    for i in ciphers:
        scored_ciphers.append([i, chi2_score(i)])
    scored_ciphers.sort(key = itemgetter(1))
    return scored_ciphers 

#creates table of all XORs, finds key corresponding to each val
def get_keys(str1, retvals):
    hex_data = str1.decode("hex")
    lookup = []
    indices = []
    for i in xrange(256):
        array = bytearray(hex_data)
        for j in xrange(len(array)):
            array[j] ^= i
        lookup.append(str(array))
    for word in retvals:
        try:
            indices.append(hex(lookup.index(word)))
        except:
            indices.append("KEY NOT FOUND")
    return indices

#to be called by user
#returns list of the N most like decryptions of str1 (hex) with corresponding keys
def printNtranslations(str1, N):
    dictvals = dict_scores(str1)
    retvals = []
    if N > len(dictvals):
        N = len(dictvals)
    for i in xrange(N):
        retvals.append(dictvals[i][0])
    return zip(*[retvals, get_keys(str1, retvals)])

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
        key = [printNtranslations(block,1)[0][1][2:].zfill(2) for block in blocks]
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
