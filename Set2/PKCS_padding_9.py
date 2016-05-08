def pad(string, blocksize):
    numbytes = blocksize - len(string) % blocksize
    if numbytes == 0:
        numbytes = blocksize
    #If the original data is a multiple of N bytes,
    #then an extra block of bytes with value N is added.
    formatted = str(hex(numbytes))[2:]
    if len(formatted) == 1:
        formatted = "0" + formatted
    padding = "".join([formatted]*numbytes)
    return string + padding

print pad("YELLOW SUBMARINE",16)
