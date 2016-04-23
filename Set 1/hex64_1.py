import base64
import binascii

base16 = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
binary = binascii.unhexlify(base16)
base64 = binascii.b2a_base64(binary)

print base64
