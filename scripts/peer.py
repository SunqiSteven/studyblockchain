
import hashlib
import time,random
import os
from config import ( config )
from exceptions import ( VMError )

def random_key():
    key = os.urandom(32).hex() \
        + str(random.randrange(2**256-1)) \
        + str(time.time() * 1000)
    h_func = hashlib.sha256()
    h_func.update(key.encode('utf-8'))
    return h_func.hexdigest()





