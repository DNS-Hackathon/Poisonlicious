#!/usr/bin/env python3

"""This is an experimentation for the poisonlicious project. It
resolves a name then send it to the configured peer."""

# https://www.dnspython.org/
import dns.message
import dns.query
import dns.rdata
import dns.rdataclass
import dns.tsigkeyring
import dns.resolver

import sys
import socket

verbose = True

# Poisonlicious peer
PEER = "10.13.38.180"
PORT = 53535

def usage(msg=None):
    if msg is not None:
        print(msg, file=sys.stderr)
    print("Usage: %s domain-name [dns-record-type]" % sys.argv[0])

def query(qname, qtype=dns.rdatatype.AAAA, server=dns.resolver.get_default_resolver()._nameservers[0]):
    """Qname and qtype MUST be int, not strings. Returns a tuple {result,
       value, ttl}."""
    if verbose:
        print("Querying %s/%s at %s" % (qname, dns.rdatatype.to_text(qtype), server))
    msg = dns.message.make_query(qname, qtype,
                                 use_edns=0, want_dnssec=False, payload=4096)
    reply = dns.query.udp(msg, server, timeout=2)
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
    
if len(sys.argv) > 3 or len(sys.argv) < 2:
    usage()
    sys.exit(1)
qname = dns.name.from_text(sys.argv[1])
if len(sys.argv) == 2:
    qtype = dns.rdatatype.AAAA
else:
    qtype = dns.rdatatype.from_text(sys.argv[2])
r = query(qname, qtype)
(status, data, ttl) = r
if status != "OK":
    print("Cannot get information on %s/%s: %s" % (qname, qtype, status))
    sys.exit(1)
print("Value of %s/%s is %s" % (qname, dns.rdatatype.to_text(qtype), r))
keyring = dns.tsigkeyring.from_text({
    "foobar-example-dyn-update." : "WS7T0ISoaV+Myge+G/wemHTn9mQwMhDGMwmTlJ3xcXRCJ6v1EVkNLlIvvah+2erWjz1v0mBW2NPKArcWHENtuA=="
})
msg = dns.message.make_response(dns.message.make_query(qname, qtype,
                                                       use_edns=0, want_dnssec=False, payload=4096))
msg.use_tsig(keyring)
rrset = msg.get_rrset(
    msg.answer, qname, dns.rdataclass.IN, qtype, create=True, force_unique=True)
rrset.add(data, ttl)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sending to %s:%s" % (PEER, PORT))
sock.sendto(msg.to_wire(), (PEER, PORT))
