import json
import hashlib

def gerarHash(jsonstr):
    h = hashlib.new('ripemd160')
    h.update(jsonstr.encode())
    return h.hexdigest()