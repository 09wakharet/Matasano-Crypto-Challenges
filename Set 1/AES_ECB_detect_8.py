import base64, binascii, collections
from Crypto.Cipher import AES
#documentation at https://www.dlitz.net/software/pycrypto/api/2.6/

key = "YELLOW SUBMARINE"
aes = AES.new(key, AES.MODE_ECB)

textfile = open("challenge8.txt","r").read()
ciphertexts = [line for line in textfile.splitlines()]#array of hex ciphers

max = 0
encypted = ''

for cipher in ciphertexts:
    chunks = [cipher[i:i+32] for i in range(0, len(cipher), 32)]
    counter = collections.Counter(chunks)
    temp = counter.most_common(1)[0][1]
    if temp > max:
        max = temp
        encrypted = cipher

print max, encrypted
