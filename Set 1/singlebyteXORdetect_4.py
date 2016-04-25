import binascii, base64
import singlebyteXOR_3 as xor

test = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

possible = []
count = 0
file = open("challenge4.txt","r").read()
for line in file.splitlines():
    vals = xor.printNtranslations(line,256)
    if vals:
        possible.append(vals)
        print line

print count
for i in possible:
    for j in i:
        print j


#key is 0x58, check if it is being XORed correctly
