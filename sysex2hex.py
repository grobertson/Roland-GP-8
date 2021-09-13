from binascii import hexlify

file = open("sysex_to_read.syx",rb)

content = bytearray(file.read())

close(file)
print(content) 
