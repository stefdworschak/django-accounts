import hashlib


def hashstring(string, length=10):
    """ Hashes a string using the sha265 algorithm

    Returns a substring of the hash's hexdigest """
    base_hash = hashlib.sha256()
    username_in_bytes = bytes(string, 'utf-8')
    base_hash.update(username_in_bytes)
    return base_hash.hexdigest()[:length]