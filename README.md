# Poisonlicious

When an organisation operates a big network of DNS resolvers \[[RFC1034](https://www.rfc-editor.org/info/rfc1034)\] \[[RFC1035](https://www.rfc-editor.org/info/rfc1035)\], for instance for an important public resolver \[[RFC9499](ihttps://www.rfc-editor.org/info/rfc9499)\] ([Section 6](https://www.rfc-editor.org/rfc/rfc9499.html#name-dns-servers-and-clients)), it may be a performance improvment to distribute the result of the resolution process between the resolvers.
This project implements a way to to do so, using blockchains (just kidding) and unicast messages to a set of pre-configured peers.

Links:

- [Poisonlicious version of the Unbound resolver](https://github.com/DNS-Hackathon/unbound-poisonlicious)
- [Draft pull request at the NLnet Labs Unbound repository](https://github.com/NLnetLabs/unbound/pull/1250)
- [Editor's copy of the draft](https://dns-hackathon.github.io/Poisonlicious/)
- [Presentation](https://dns-hackathon.github.io/Poisonlicious/cache-poisonlicious-presentation.html)
