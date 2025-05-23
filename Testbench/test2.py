mem = bytearray(8)
a = (0x12345678).to_bytes(4, byteorder='little')
a = a[::-1]
print(a)