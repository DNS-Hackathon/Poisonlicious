#!/usr/bin/env python3

"""This is an experimentation for the poisonlicious project. It uses
Afnic's open data to create a lot of DNS messages with .fr data and
store them in a file.

"""

# https://www.dnspython.org/
import dns.message
import dns.query
import dns.rdata
import dns.rdataclass
import dns.tsigkeyring
import dns.resolver

import sys
import csv
import struct

INPUTFILENAME = "OPENDATA_A-NomsDeDomaineEnPointFr.csv"
OUTPUTFILENAME = "afnic.dnsbin"

# Poisonlicious peer
KEYNAME = None
#KEYNAME = "foobar-example-dyn-update."
KEYVALUE = None
#KEYVALUE = "WS7T0ISoaV+Myge+G/wemHTn9mQwMhDGMwmTlJ3xcXRCJ6v1EVkNLlIvvah+2erWjz1v0mBW2NPKArcWHENtuA=="
MAX = 100000

def usage(msg=None):
    if msg is not None:
        print(msg, file=sys.stderr)
    print("Usage: %s" % sys.argv[0])

def query(qname, qtype=dns.rdatatype.AAAA, server=dns.resolver.get_default_resolver()._nameservers[0]):
    """Qname and qtype MUST be int, not strings. Returns a tuple {result,
       value, ttl}."""
    msg = dns.message.make_query(qname, qtype,
                                 use_edns=0, want_dnssec=False, payload=4096)
    try:
        reply = dns.query.udp(msg, server, timeout=0.4)
    except dns.exception.Timeout:
        return("TIMEOUT", None, None)
    if reply.rcode() == dns.rcode.NXDOMAIN:
        return ("NXDOMAIN", None, None)
    elif reply.rcode() == dns.rcode.SERVFAIL:
        return ("SERVFAIL", None, None) 
    elif reply.rcode() == dns.rcode.REFUSED:
        return ("REFUSED", server, None)
    elif reply.rcode() != dns.rcode.NOERROR:
        return ("UNKNOWN ERROR", reply.rcode(), None)
    answer = reply.get_rrset(dns.message.ANSWER, qname, dns.rdataclass.IN, qtype)
    if answer is None:
        answer = reply.get_rrset(dns.message.ANSWER, qname, dns.rdataclass.IN, dns.rdatatype.CNAME)
        if answer is None:
            return ("NODATA", None, None)
    return ("OK", answer[0], answer.ttl)
    
if len(sys.argv) > 1:
    usage()
    sys.exit(1)

qtype = dns.rdatatype.A
if KEYNAME is not None:
    keyring = dns.tsigkeyring.from_text({
        KEYNAME : KEYVALUE
    })
csvfile = open(INPUTFILENAME)
output = open(OUTPUTFILENAME, 'wb')
reader = csv.reader(csvfile, delimiter=';') 
headers = True
stored = 0
total = 0
for row in reader:
    if not headers:
        deleted = row[11]
        if deleted is None or deleted == "":
            total += 1
            name = row[0]
            qname = dns.name.from_text(name)
            r = query(qname, qtype)
            (status, data, ttl) = r
            if status != "OK":
                continue
            msg = dns.message.make_response(dns.message.make_query(qname, qtype,
                                                                   use_edns=0, want_dnssec=False, payload=4096))
            if KEYNAME is not None:
                msg.use_tsig(keyring)
            rrset = msg.get_rrset(
                msg.answer, qname, dns.rdataclass.IN, qtype, create=True, force_unique=True)
            try:
                rrset.add(data, ttl)
            except dns.rdataset.IncompatibleTypes:
                rrset = msg.get_rrset(
                    msg.answer, qname, dns.rdataclass.IN, 'CNAME', create=True, force_unique=True)        
            binary = msg.to_wire()
            output.write(struct.pack("!I", len(binary)))
            output.write(binary)
            stored += 1
            if stored > MAX:
                break
            if (stored % 1000) == 0:
                print("%i domains, %i messages stored" % (total, stored))
    else:
        headers = False
output.close()
