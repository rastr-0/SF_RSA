import math
from random import randint
import timeit


class Prime:
    """This class stands for implementing the process of generating big high-probability prime number"""
    @staticmethod
    def generate_prime_sequence(sequence_size: int) -> list:
        """The sequence of the prime numbers is generated for discarding numbers
            that are the multiplication of a prime number.
        Here is used eratosthenes sieve for generating small primes up to prime_bits_size * 10"""
        sequence_size *= 10

        is_prime = [True] * sequence_size
        i = 2
        while i*i < sequence_size:
            if is_prime:
                for j in range(i*i, sequence_size, i):
                    is_prime[j] = False
            i += 1

        primes = list()
        for i in range(2, sequence_size):
            if is_prime[i]:
                primes.append(i)

        return primes

    @staticmethod
    def __is_not_divisible_by_small_prime(candidate: int, prime_sequence: list) -> bool:
        for prime in prime_sequence:
            if candidate % prime == 0:
                return False
        return True

    @staticmethod
    def __bytes_to_bits(num_bytes: bytes) -> str:
        """Iterates over the list of given bytes, converts each byte to 8 bits, and joins them into a string."""
        return ''.join(f'{byte:08b}' for byte in num_bytes)

    @staticmethod
    def __get_random_bits(length: int) -> str:
        """Reads N random bits from the pseudorandom generator via the file /dev/urandom in UNIX."""
        # (length + 7) // 8 ensures that the bits are correctly converted to bytes for lengths not multiples of 8
        return Prime.__bytes_to_bits(num_bytes=open("/dev/urandom", "rb").read((length + 7) // 8))

    @staticmethod
    def __is_prime(candidate: int) -> bool:
        """Miller-Rabin primality test. This algorithm tests 2 equalities:
            (base^d) = 1 mod candidate
            Exists r < s in Z, such that ((a^2)^r)d = -1 mod n
        If at least one of the equalities is not satisfied, then the candidate is a composite number"""

        """Each randomly selected base gives 25% of error, in order to have a sufficient measure of confidence, than
            number is not composite, tests with different bases should be run at least log2(candidate) times"""
        if candidate < 2:
            return False
        if candidate in (2, 3):
            return True

        # represent candidate - 1 in the following form: (candidate-1) = 2^t mod candidate
        s = 0
        t = candidate - 1
        while t % 2 == 0:
            t //= 2
            s += 1

        number_of_tests = math.floor(math.log2(candidate))
        for _ in range(0, number_of_tests):
            base = randint(2, candidate - 2)
            # base^t mod candidate
            x = pow(base, t, candidate)
            if x == 1 or x == candidate - 1:
                continue
            for _ in range(0, s - 1):
                # x = x^2 mod candidate
                x = pow(x, 2, candidate)
                if x == candidate - 1:
                    break
            else:
                return False

        return True

    @staticmethod
    def generate_prime(prime_bits_size: int) -> int:
        primes = Prime.generate_prime_sequence(prime_bits_size)
        while True:
            candidate = Prime.__get_random_bits(prime_bits_size)
            # Ensure that the highest and the last bits are 1 (number is big and odd).
            # This can be done more efficiently with bit masking.
            candidate = '1' + candidate[1:-1] + '1'
            # Convert bits to int.
            candidate = int(candidate, 2)

            if Prime.__is_not_divisible_by_small_prime(candidate, primes) and Prime.__is_prime(candidate):
                return candidate


class RSA:
    """This class stands for implementation public and private keys generation, encryption and decryption
        Key Generation (2048 bits example):
            1) Generate two 1024 bits primes
            2) Compute multiple of two primes
            3) Hard-code a public exponent (65537 is quite a secure choice, another popular options are 3 or 17)
            4) Calculate euler_function(prime1 - 1, prime2 - 1)
            5) Calculate private exponent with extended Euclidean algorithm
            6) Save private key and return public key
        Encryption:
            1) Convert given string to bytes and then to int
            2) Calculate given_string^public_key mod composite_of_2_primes
        Decryption:
            1) Calculate int number from given encrypted int: encrypted^private_key mod composite_of_2_primes
            2) Convert int to bytes and then to string"""
    def __init__(self, key_size):
        self.__private_key = None
        self.key_size = key_size

    @staticmethod
    def __euler_function(first_prime: int, second_prime: int) -> int:
        return (first_prime - 1) * (second_prime - 1)

    @staticmethod
    def __extended_euclidean(a: int, b: int) -> (int, int, int):
        """Find GCD, x and y in R for the following equation:
            ax + by = GCD(a, b)"""
        x0, x1 = 1, 0
        y0, y1 = 0, 1
        while b != 0:
            q = a // b
            a, b = b, a % b
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        # a = GCD(a, b), x0 and y0 are Bezout coefficients
        return a, x0, y1

    @staticmethod
    def __generate_private_exponent(public_exponent: int, phi: int) -> int:
        """Generate private_exponent for the following equation:
            private_exponent = public_exponent^(-1) mod phi"""
        gcd, x, _ = RSA.__extended_euclidean(public_exponent, phi)
        return x % phi

    def generate_keys(self) -> tuple[int, int]:
        """Generate public and private RSA keys and return public, save private to the class variable"""
        first_prime = Prime.generate_prime(self.key_size // 2)
        second_prime = Prime.generate_prime(self.key_size // 2)
        composite = first_prime * second_prime
        # public exponent (recommended public exponent value, 3 and 17 are also popular values)
        public_exponent = 65537
        # phi value
        phi = RSA.__euler_function(first_prime, second_prime)
        # private exponent
        private_exponent = RSA.__generate_private_exponent(public_exponent, phi)

        self.__private_key = (private_exponent, composite)
        # function returns public key
        return public_exponent, composite

    @staticmethod
    def encrypt(text: str, public_key: tuple[int, int]) -> int:
        text_bytes_rep = bytes(text, "UTF-8")
        public_exponent, composite = public_key
        return pow(int.from_bytes(text_bytes_rep, byteorder='big'), public_exponent, composite)

    def decrypt(self, encrypted_text: int) -> str:
        private_exponent, composite = self.__private_key
        decrypted_int = pow(encrypted_text, private_exponent, composite)
        decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder="big")
        return decrypted_bytes.decode("UTF-8")


start = timeit.default_timer()

rsa = RSA(2048)
your_public_key = rsa.generate_keys()
encrypted = rsa.encrypt("This is text for encryption", your_public_key)
print(rsa.decrypt(encrypted))

print(f"The time spent for generating prime: {timeit.default_timer() - start}")
