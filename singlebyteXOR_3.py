import binascii, base64
import collections

test = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

#TODO return key

#str1 is a hex string, byte a hex byte
#returns a valid ascii string
#throws away strings with non-english characters (returns none)
def xor_byte(str1, byte):
    hex_data = str1.decode("hex")
    array = bytearray(hex_data)
    for i in xrange(len(array)):
        array[i] ^= int(byte,16)
        if array[i]>126 or array[i]<32:
            return
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
        v = temp[k]
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
            ignored+=1
            break
        obs = float(frequencies[k])
        exp = float(english_freq[k]*len(str1))
        chi2 += pow(obs-exp,2)/exp
    return chi2 * (1 + ignored/len(str1))

#TODO rewrite the last two methods, it's all indexing stuff
def dict_scores(str1):
    ciphers = []
    for i in xrange(256):
        temp = xor_byte(test,hex(i))
        if temp is not None:
            ciphers.append(temp)
    scored_ciphers = {}
    for i in ciphers:
        scored_ciphers[chi2_score(i)] = i
    return scored_ciphers 

def printNtranslations(str1, N):
    dictvals = dict_scores(str1)
    sortedvals = sorted(dictvals)
    vals = []
    for key in sortedvals:
        vals.append(dictvals[key])
        if (len(vals)>N):
            break
    return vals

vals = printNtranslations(test,3)
for val in vals:
    print val
