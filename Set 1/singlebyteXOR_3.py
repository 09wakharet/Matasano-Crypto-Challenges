import binascii, base64
import collections
from operator import itemgetter

test = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
#str1 is a hex string, byte a hex byte
#returns a valid ascii string
#throws away strings with non-english characters (returns none)
def xor_byte(str1, byte):
    hex_data = str1.decode("hex")
    array = bytearray(hex_data)
    for i in xrange(len(array)):
        array[i] ^= int(byte,16)
        if array[i]>126 or array[i]<32:
            return#TODO update which values are thrown out - allow specials chars
    return str(array)

#naive letter frequency analysis
def naive_score(str1):
    frequencies =  collections.Counter(str1)
    score = 0
    #+3 for etaonri
    #+2 shrdlu
    #+1 for other alphanumeric text
    #-1 for non-alphanumeric text
    ref1 = list("eatonri")
    ref2 = list("shrdlu")
    ref3 = list("bcfgjkmnpqvwxyz0123456789")
    for k in frequencies:
        v = frequencies[k]
        if k in ref1:
            score += 3*v
        elif k in ref2:
            score += 2*v
        elif k in ref3:
            score += v
        else:
            score -= v
    return score

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
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies =  collections.Counter(str1)
    chi2 = 0.
    ignored = 0.
    for k in frequencies:
        if k not in alphabet:
            ignored+=frequencies[k]
            break
        obs = float(frequencies[k])
        exp = float(english_freq[k]*len(str1))
        chi2 += pow(obs-exp,2)/exp
    return (chi2 + ignored/len(str1)) * (1 + ignored/len(str1))

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

#vals =  printNtranslations(test,256)
#vals = dict_scores(test)
#for string in vals:
#    print string
