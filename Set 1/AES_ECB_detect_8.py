import base64, binascii
from Crypto.Cipher import AES
#documentation at https://www.dlitz.net/software/pycrypto/api/2.6/

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)

textfile = open("challenge8.txt","r").read()
ciphertexts = [line for line in textfile.splitlines()]#array of hex ciphers
