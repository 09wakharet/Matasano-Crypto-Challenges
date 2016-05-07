def pad(string, length):
    numbytes = length - len(string)
    if numbytes < 0:
        Exception("desired length less than message length")
    formatted = str(hex(numbytes))[2:]
    if len(formatted) == 1:
        formatted = "0" + formatted
    padding = "".join([formatted]*numbytes)
    return string + padding

print pad("YELLOW SUBMARINE",20)
