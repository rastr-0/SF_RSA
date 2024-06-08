# SF_RSA
Simple and Fast RSA implementation with hand-written prime numbers generation in Python.
## Prime numbers Generation
For generating prime numbers is used Miller-Rabin algorithm and checking for divisibility by a sequence of small primes generated with Eratosthenes Sieve. Random bits are get from /dev/urandom file in Unix.
## RSA
#### Key Generation (2048 bits example):
```
1) Generate two 1024 bits primes
2) Compute multiple of two primes
3) Hard-code a public exponent (65537 is quite a secure choice, another popular options are 3 or 17)
4) Calculate euler_function(prime1 - 1, prime2 - 1)
5) Calculate private exponent with extended Euclidean algorithm
6) Save private key and return public key
```
#### Encryption:
```
1) Convert given string to bytes and then to int
2) Calculate given_string^public_key mod composite_of_2_primes
```
#### Decryption:
```
1) Calculate int number from given encrypted int: encrypted^private_key mod composite_of_2_primes
2) Convert int to bytes and then to string
```
## Tests
Tests were done on my laptop (Ryzen 5 5600H, 24Gb RAM) with different RSA keys sizes:
* 512 bits RSA keys
```
Test (0): 0.05203962099949422
Test (1): 0.04846767700109922
Test (2): 0.0652224989989918
Test (3): 0.05349613099861017
Test (4): 0.054369544001019676
Test (5): 0.05666580400065868
Test (6): 0.05314915300004941
Test (7): 0.05707518000053824
Test (8): 0.056296883998584235
Test (9): 0.05772694400002365
```
* 1024 bits RSA keys:
```
Test (0): 0.46605865599849494
Test (1): 0.4654594650000945
Test (2): 0.45704866600135574
Test (3): 0.47402370199961297
Test (4): 0.48767767200115486
Test (5): 0.49173967099886795
Test (6): 0.49617687499994645
Test (7): 0.4839278710005601
Test (8): 0.46782631399946695
Test (9): 0.502362852999795
```
* 2048 bits RSA keys
```
Test (0): 5.601344878001328
Test (1): 5.271162814999116
Test (2): 5.432002318000741
Test (3): 5.471853471999566
Test (4): 5.845398714000112
Test (5): 5.5919270729991695
Test (6): 5.4350055110007816
Test (7): 5.908701343998473
Test (8): 5.602632273999916
Test (9): 5.470917590999306
```
