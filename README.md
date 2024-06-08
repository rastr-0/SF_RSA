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
Tests were done on my laptop (Ryzen 5 5600H, 24Gb RAM) with different RSA keys sizes and random 50 characters generated text:
* 512 bits RSA keys
```
Test (0): 0.0497
Test (1): 0.0568
Test (2): 0.0539
Test (3): 0.0514
Test (4): 0.0488
Test (5): 0.052
Test (6): 0.0666
Test (7): 0.0493
Test (8): 0.0431
Test (9): 0.0449
```
* 1024 bits RSA keys:
```
Test (0): 0.5015
Test (1): 0.5473
Test (2): 0.4703
Test (3): 0.4644
Test (4): 0.4739
Test (5): 0.4763
Test (6): 0.4934
Test (7): 0.5064
Test (8): 0.4752
Test (9): 0.4845
```
* 2048 bits RSA keys
```
Test (0): 5.3541
Test (1): 5.4394
Test (2): 5.3898
Test (3): 5.5832
Test (4): 5.5234
Test (5): 5.7171
Test (6): 5.8348
Test (7): 5.5278
Test (8): 5.4383
Test (9): 5.4908
```
