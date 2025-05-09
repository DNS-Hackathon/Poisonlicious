---
title: Cache Poisonlicious
tags: [Talk]
marp: true
theme: gaia
class:
    - lead
    - invert
---

# Cache Poisonlicious
## Babak/Moin/Stéphane/Willem
https://github.com/DNS-Hackathon/Poisonlicious

---

## Problem Statement

---

## Large Scale Public DNS Resolvers

- Multiple resolvers running in the same administrative domain

- Resolvers are oblivious to the content of other resolvers' cache

- A resolver must perform full resolution for a request, even though the answer is most likely known and cached by another resolver in the same cluster.

---

## Key Issue

- **Cold Resolver:** A new or inactive resolver has to query the authoritative servers, leading to longer response times and unnecessary traffic.

- **Caching:** Existing resolvers in the cluster might already have the data but cannot share it.

---

## Cache Warm up

![width:1024px](https://hackmd.io/_uploads/SkikqfN2kl.png)

---

## Why It Matters

- **DNS Traffic:** Constant requests to authoritative DNS servers increase internet traffic and strain the infrastructure.

- **Warm-Up Delays:** New resolvers (or cold resolvers) need time to populate their caches, causing slower responses.

- **Efficiency Reduction:** Without data sharing between resolvers, the system becomes inefficient when the same queries are made frequently.

- **Environmental Impact:** More workload for the resolver, the authoritative servers and the network.

---

## The Proposed Solution:
### Cache Update Sharing Across Resolvers

---

## Data Sharing Mechanism

- When a resolver encounters a new authoritative answer, it shares it with other resolvers in the same cluster in the **DNS Wire Format**.

- Allows seamless communication between resolvers in the same cluster.
  
---

## Challenges

---

### Integrity

- Ensuring that cached data shared between resolvers is accurate and up-to-date.

---

### Security

- Security concerns like cache poisoning are not considered as we assume the system operates within an autonomous boundary, reducing the risk of malicious activity.

---

### Noise

- A resolver with a cold cache can pollute communication channel.

---

### Scalability

- Designing the system to handle a high volume of requests and data sharing efficiently.

---

## Achievement in Hackathon

- Drafted an RFC
- Proof-of-concept implementation in Unbound

---

## Key Takeaways

- By sharing cached DNS data in the DNS wire format, DNS resolvers can serve data faster, reduce unnecessary Authoritative DNS queries, and improve overall system and network efficiency.

- The approach helps DNS networks scale more efficiently while keeping the internet’s DNS traffic sustainable.

---

## Next Steps

1. **Testing & Security** - Implement tests to ensure data accuracy and address security concerns.

2. **Functional Tests** - Study different scenarios in a lab (or production) environment.

3. **Deployment** - Gradually roll out the system to a subset of DNS resolvers.

4. Work with the community in IETF meetings to make this a formal standard.

---

### Let's Build a More Efficient DNS Infrastructure!
