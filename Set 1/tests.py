import binascii
import base64


test = "5f73737775727b3c515f3b6f3c707577793c7d3c6c736972783c737a3c7e7d7f7372"
test = "3915151113141d5a37395d095a1613111f5a1b5a0a150f141e5a151c5a181b191514"
print len(test)
print len(binascii.unhexlify(test))

def testfunc(a):
    return a*a

def nestedfunc(a):
    b = testfunc(a)
    return b*b
