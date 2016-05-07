import base64, binascii
from Crypto.Cipher import AES
#documentation at https://www.dlitz.net/software/pycrypto/api/2.6/

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)

textfile = open("challenge7.txt","r").read()
ciphertext = "".join([line for line in textfile.splitlines()])
ciphertext = base64.b64decode(ciphertext)
message = cipher.decrypt(ciphertext)
print message
