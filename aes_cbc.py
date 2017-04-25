#!/usr/bin/python
#Solution for the Awkward Ending Syndrome - it uses AES CBC with an IV of 16 NULL bytes
from Crypto.Cipher import AES
import binascii

key = binascii.unhexlify('000102030405060708090A0B0C0D0E0F')
iv = binascii.unhexlify('00000000000000000000000000000000')
ciphertext = binascii.unhexlify('3B953347892900C95858A5C16FD8DFB0920DF37294CBC3313AAB85608D32328D')

obj = AES.new(key, AES.MODE_CBC, iv)
plaintext = obj.decrypt(ciphertext)

print plaintext
