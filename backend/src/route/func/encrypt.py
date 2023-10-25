from hashlib import sha256, md5

def encrypt_string(hash_string, type="sha256"):
    if type == "sha256":
        sha_signature = \
            sha256(hash_string.encode()).hexdigest()
    elif type == "md5":
        sha_signature = \
            md5(hash_string.encode()).hexdigest()
    return sha_signature