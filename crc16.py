#!/usr/bin/env python

import os, sys

from array import array
def crc16(string, value=0):
    """ Single-function interface, like gzip module's crc32
    """
    for ch in string:
        value = table[ord(ch) ^ (value & 0xff)] ^ (value >> 8)
    return value

class CRC16(object):
    """ Class interface, like the Python library's cryptographic
        hash functions (which CRC's are definitely not.)
    """

    def __init__(self, string=''):
        self.val = 0
        if string:
            self.update(string)

    def update(self, string):
        self.val = crc16(string, self.val)

    def checksum(self):
        return chr(self.val >> 8) + chr(self.val & 0xff)

    def hexchecksum(self):
        return '%04x' % self.val

    def copy(self):
        clone = CRC16()
        clone.val = self.val
        return clone

# CRC-16 poly: p(x) = x**16 + x**15 + x**2 + 1
# 0001 1000 0000 0000 0101 => 0x8005 (MSB)
# 1010 0000 0000 0001 1000 => 0xa001 (LSB)
# top bit implicit, reflected
#poly = 0xa001
poly = 0x8005
table = array('H')
for byte in range(256):
    crc = 0
    for bit in range(8):
        if (byte ^ crc) & 1:
            crc = (crc >> 1) ^ poly
        else:
            crc >>= 1
        byte >>= 1
    table.append(crc)

if __name__=="__main__":
    check_string = "123456789"
    #check_sum = 0xbb3d
    check_sum = 0xafad

    crc = CRC16()
    crc.update(check_string)
    gen_sum = int("0x"+crc.hexchecksum(),16)

    print "Check string '%s'. Calculated CRC16 '0x%04x', expected CRC16 '0x%04x'." % (check_string,gen_sum,check_sum)
    assert gen_sum == check_sum, "ERROR: CRC16 check sum mis-match: %d != %d" % (check_sum,gen_sum)
