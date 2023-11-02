import hashlib
import random
import string


def get_random_string(length=12):
    """
    Generates a random string of specified length.

    Returns: Random string of specified length.
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """
        Hashes a password using PBKDF2 algorithm.

        Args:
            password (str): Password to hash.
            salt (str): Salt to use for hashing. If None, a random salt is generated.

        Returns:
            str: Hashed password string.
        """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """
        Validates a password against a hashed password.

        Args:
            password (str): Password to validate.
            hashed_password (str): Hashed password string.

        Returns:
            bool: True if password matches the hashed password, False otherwise.
        """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed
