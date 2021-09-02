import os
from hashlib import blake2b
msg = b'some message'
# Calculate the first hash with a random salt.
salt1 = os.urandom(blake2b.SALT_SIZE)
print(salt1.hex())
h1 = blake2b(salt=salt1)
h1.update(msg)
print(h1.hexdigest())
# Calculate the second hash with a different random salt.
salt2 = os.urandom(blake2b.SALT_SIZE)
h2 = blake2b(salt=salt2)
h2.update(msg)
print(h2.hexdigest())
