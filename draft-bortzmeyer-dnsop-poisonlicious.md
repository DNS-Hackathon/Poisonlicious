---
title: Synchronizing caches of DNS resolvers
abbrev: Poisonlicious
category: exp

docname: draft-bortzmeyer-dnsop-poisonlicious-02
submissionType: IETF
number:
date:
consensus: true
v: 3
area: General
workgroup: DNSOP Working Group
keyword:
  - DNS
  - DNSSEC
  - optimization
  - caching
venue:
  group: dnsop
  type: Working Group
  mail: dnsop@ietf.org
  arch: https://mailarchive.ietf.org/arch/browse/dnsop/
  github: https://github.com/DNS-Hackathon/Poisonlicious
  latest:

author:
  -
    fullname: Stéphane Bortzmeyer
    initials: S.
    surname: Bortzmeyer
    org: Afnic
    street: 7 avenue du 8 mai 1945
    city: Guyancourt
    code: 78280
    country: FR
    email: bortzmeyer+ietf@nic.fr
    uri: https://www.afnic.fr/
  -
    fullname: Willem Toorop
    initials: W.
    surname: Toorop
    org: NLnet Labs
    street: Science Park 400
    code: 1098 XH
    city: Amsterdam
    country: NL
    email: willem@nlnetlabs.nl
    uri: https://nlnetlabs.nl/
  -
    fullname: Babak Farrokhi
    initials: B.
    surname: Farrokhi
    org: Quad9
    street: Werdstrasse 2
    code: 8004
    city: Zürich
    country: CH
    email: babak@farrokhi.net
    uri: https://quad9.net/
  -
    fullname: Moin Rahman
    initials: M.
    surname: Rahman
    org: The FreeBSD Foundation
    street: 3980 Broadway St
    code: CO 80304
    city: Boulder
    country: US
    email: bofh@freebsd.org
    uri: https://freebsdfoundation.org/
  -
    fullname: Ondřej Surý
    initials: O.
    surname: Surý
    org: Internet Systems Consortium
    country: CZ
    email: ondrej@isc.org
  -
    fullname: Otto Moerbeek
    initials: O.
    surname: Moerbeek
    org: PowerDNS
    country: NL
    email: otto.moerbeek@powerdns.com

normative:

informative:
    MQTT:
        target: https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.docx
        title: MQTT Version 5.0
        author:
          -
            org: OASISi
        date: 2019

--- abstract

Network of cooperating and mutually trusting DNS resolvers could benefit from cache sharing, where one resolver would distribute the result of a resolution to other resolvers.
This document standardizes a protocol to do so.

--- middle

# Introduction

When an organisation operates a big network of DNS resolvers {{!RFC1034}} {{!RFC1035}}, for instance for an important public resolver {{Section 6 of !RFC9499}}, it may be a performance improvement to distribute the result of the resolution process between the resolvers.
This document standardizes how to to do so, using blockchains (just kidding) and unicast messages to a set of pre-configured peers.

TODO data from Quad9 to show that there is a caching improvement to expect.
Measuring the efficiency of caching optimizations is hard!

## Requirements Language

{::boilerplate bcp14-tagged}

## Terminology

{: vspace="0"}
Network of resolvers (TODO or resolver set? Or resolver cluster?):
: A set of resolvers working together under the same administration

Peer (or peer resolver):
: One of the other resolvers in the network

Originating resolver:
: A resolver sending data to its peers in the network

Receiving resolver (or receiving peer):
: A resolver receiving data from one of its peers in the network

Resolver:
: As used in {{Section 6 of !RFC9499}}

# The protocol

When completing a successful DNS resolution, the resolver transmits a DNS message (with the Q/R bit set, since it is a response) to the pre-configured peers, authenticating with TSIG {{!RFC8945}}.
TODO SIG0? DoT?
No acknowledgment is sent or expected.
To save work, the resolver MAY send the data only if the TTL is higher than some predefined value.

The resolver must send only data that it is sure of (for instance by DNSSEC validation or because it came with the AA bit from the queried server).
Since all of the network of resolvers are in the same organizational domain, they MUST agree on the same policy for this assessment.

Messages of this protocol are distinguished from other DNS messages by the TSIG key they use (which must therefore be specific to this protocol).
TODO or by a dedicated port?

This message MAY be the message received by the resolver from the authoritative name servers or it MAY be a new message with data composed from data already obtained by the resolver.
TODO privacy risks when sending the question section? (See {{Privacy}}

The EDNS section MUST be a new one, created to fit the needs of successful transmission to the peer.
TODO what about ECS {{?RFC7871}}

Each peer then MAY store the data in its cache.
The peer is not supposed to do DNSSEC validation (there is not always all the necessary data in the message).
TODO cache only what is in the Answer section?
See above about assessing the trustiness of the data.
TODO {{Section 5.4.1 of ?RFC2181}} talks about the ranking of data.
Should we describe it?
Since it is supposed to be used inside an organisation, where all peers trust each other, and have a consistent policy, is it necessary?
The idea is that the data is as trustworthy as if you validated it yourself.

# IANA Considerations {#IANA}

None.
\[RFC-Editor: you may delete this section\]

# Security Considerations {#Security}

The integrity and authenticity of the cached data is of course critical.
DNSSEC would help but it is not yet universally deployed and, moreover, the peer resolvers should not have to redo the validation.
So, trust between the peer resolvers is expected because it is the only way for the receiver to be sure of the data.
One way to do so is to have all of the peers under the same organisational authority, as mandated here.

For the same reason, the channel between peers must be protected, preferrably with cryptography (currently, TSIG is mandatory).
ACL and other network techniques are of course useful.

Encryption is less important than authentication since we transmit only public data.
Nevertheless, it is better to be sure that the channel between the peers is not open to snooping.

# Privacy Considerations {#Privacy}

Confidentiality is currently out of scope for this document.
The communication between the originating resolver and its receiving peers could be encrypted, for instance with DoT but it is not otherwise specified.

If the originating resolver sends the original question section in its messages to receiving peers, it can have bad privacy consequences {{?RFC9076}}
TODO: delete this section?
Replace it with dummy data?
    
# Operational Considerations {#Operation}

It is reminded that all resolvers in the network need to trust each other, probably being in the same administrative domain.
This specification is not meant to be deployed between unrelated resolvers.

The netwok of peer resolvers have to be configured out-of-band before. The way to do it is out-of-scope for this specification.

# Related and future work {#related-future}

## Related work

{{?I-D.hl-dnsop-cache-filling}} describes a mechanism to fill DNS caches with data.
The format is, like in this document, standard DNS as seen on the wire.

## Future work

### Negative answers

TODO What to do about them?
Transmit them?
(Be careful of the risk of overloading receving peers for instance when there is a dictionary attack.)
Can a receiving peer use {{?RFC8020}} and/or {{?RFC8198}} to synthetize negative answers since it did not validate data itself?

### Transport of messages

Messages could be transmitted in long-lived TCP sessions, too.

If there are 1,000 servers, sending 1,000 messages, or having a full mesh of 1,000 TCP connections may be too much.
It may be interesting to replace the unicast messages by multicast {{?RFC5110}} (the issues of multicast on the public Internet do no apply here since we envision work under only one organisation).

Is the use of a DHT reasonable?

Why not MQTT {{MQTT}} which is well suited for publish-by-one/consume-by-many?
What about protocols like protocol buffers?
TODO What about dnstap?

### Packing of messages

It could be interesting to optimize by packing the data in a C-DNS {{?RFC8618}} flow, sent with TCP (with TLS) or QUIC.
(Of course, other formats/protocols are possible.)

### Different responses

When the authoritative servers send different replies depending on the client, the various peers may send different (and under-optimized) responses to a receiving peer.

--- back

# Acknowledgements

Original idea at the DNS hackathon (RIPE-NCC / Netnod / DNS-OARC) in March 2025 at the Netnod office in Stockholm.
