# SF_RSA
Simple and Fast RSA implementation with hand-written prime numbers generation in Python.
## Description
### Prime numbers Generation
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
