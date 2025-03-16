#!/usr/bin/env python3

"""This is an experimentation for the poisonlicious project. It reads
a file of ready-to-send DNS messages and send them to a peer."""

# https://www.dnspython.org/
import dns.message
import dns.query
import dns.rdata
import dns.rdataclass
import dns.tsigkeyring
import dns.resolver

import sys
import socket
import struct

FILENAME = "afnic.dnsbin"

# Poisonlicious peer
PEER = "10.13.38.180"
PORT = 53535
KEYNAME = None
#KEYNAME = "foobar-example-dyn-update."
KEYVALUE = None
#KEYVALUE = "WS7T0ISoaV+Myge+G/wemHTn9mQwMhDGMwmTlJ3xcXRCJ6v1EVkNLlIvvah+2erWjz1v0mBW2NPKArcWHENtuA=="

def usage(msg=None):
    if msg is not None:
        print(msg, file=sys.stderr)
    print("Usage: %s" % sys.argv[0])

if len(sys.argv) > 1:
    usage()
    sys.exit(1)

qtype = dns.rdatatype.A
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
input = open(FILENAME, "rb")
sent = 0
over = False
format = "!I"
while not over:
    data = input.read(struct.calcsize(format))
    if len(data) == 0:
        over = True
        break
    (size,) = struct.unpack(format, data)
    msg = input.read(size)
    sock.sendto(msg, (PEER, PORT))
    sent += 1
    if (sent % 1000) == 0:
        print("%i messages sent" % (sent))
    
