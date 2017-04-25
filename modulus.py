#!/usr/bin/python

s = "flagc".encode("hex")
i = int(s, 16)
modulus = i % 16

print modulus
