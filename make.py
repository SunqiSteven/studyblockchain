#!/usr/bin/python
# coding=utf-8
import argparse
import base64,hashlib,time
import os,sys
import binascii,random

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-port',help='server port',default='8764',type=int)
parser.add_argument('-f',help='package',action="store_true",dest="mine")
args = parser.parse_args()

# seed = os.urandom(32).hex()
# seed_64 = base64.b64encode(seed.enco  de('utf-8'))
# print(seed_64.decode('utf-8'))    
# seed_64 = 'ODM4NTQ3NmFhNTU3Mzc2ZGU5MjQ2N2JiOGJlZWY0OTY5MGEzMzE0YzQ5YTQxNjAzOGY5ZDczOWI0ODk5Y2JhYg==';
# print(base64.b64decode(seed_64).decode('utf-8'))
# print(binascii.b2a_hex(seed_64))
# print(bin(256))
# print(sys.version_info)

def sha256(msg):        
    h = hashlib.sha256()
    h.update(msg.encode('utf-8'))
    return h.hexdigest()

def random_key():
    key = str(os.urandom(32).hex()) \
        + str(random.randrange(2**256)) \
        + str(int(time.time() * 10000))
    return sha256(key)

def hash_to_int(hash):
    return int(hash,16)

# msgHash = '9d6b68cfdc1f6d657e0328bf89d8c02b2c478eb64b142f63be29f049d104d1eb'
# print(hash_to_int(msgHash))
# Elliptic curve parameters (secp256k1)
P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7           
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)


# a, p = 8 , 10
# print(round(2.888))


# // 2**3 * 1 + 2**2 * 1 + 2    **1*0 + 2**0*1 = 8 + 4 + 0 + 1 = 13 = 1101
# // 2**2*1 + 2**1*1 + 2**0*0 +       0.5     = 4 + 2      = 6.5 = 110
import server

# server.run(args.port)



    assert isinstance(v,int)
    print(v)

create('20')










