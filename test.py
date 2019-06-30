
import hashlib
import time
import json

import _thread

from aiohttp import web

def hash_sha256(data_bytes):
    h = hashlib.sha256()
    h.update(data_bytes)
    return h.hexdigest()

class CREATE_TX_ERROR(Exception):
    pass    

"""
    block
"""
class Block():
    def __init__(self,timestamp,merkle_root,previous_block,nonce,trx,block_hash):
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.previous_block = previous_block
        self.trx = trx
        self.block_hash = block_hash
    @classmethod
    async def getBlockByHeight(self,request):
        current_blocks_len = len(BLOCK_CHAIN)
        height = request.match_info.get('height',current_blocks_len-1)
        height = int(height)
        if height > current_blocks_len -1:
            rspData = {'success':'fail','msg':'not exits'}
        else:
            rspData = BLOCK_CHAIN[height]
        resp = web.json_response(rspData)
        return resp

"""
    Transaction
"""
class Tx():
    def __init__(self,from_address,to_address,value):
        self.from_address = from_address
        self.to_address = to_address
        self.value = value
        self.timestamp = round(time.time())
        # self.txHash = self.getTxHash()
    def getTxHash(self):
        return hash_sha256((self.from_address \
            + self.to_address \
            + str(self.timestamp) \
            + str(self.value)).encode('utf-8'))
    def toJson(self):
        tx_dict = {
            'from_address':self.from_address,
            'to_address':self.to_address,
            'value': self.value
        }
        return json.dumps(tx_dict)
    @classmethod
    def calc_merkle_root(self,trx):
        if len(trx) == 0:
            return ''
        if len(trx) % 2 != 0:
            trx.append(trx[len(trx) - 1])
        while len(trx) > 1:
            temp = []
            for i in range(len(trx)):
                if i % 2 == 0 and i+1 < len(trx):
                    _hash = hash_sha256((trx[i] + trx[i+1]).encode('utf-8'))
                    temp.append(_hash)
            if len(temp) % 2 != 0 and len(temp) > 1:
                temp.append(temp[-1])      
            trx = temp
        return trx[0]
    @classmethod
    async def  create_tx(self,request):
        data = await request.content.read()
        try:
            trx_data = json.loads(data.decode('utf-8'))
        except:
            return web.json_response({'status':"fail",'msg':'params format error'})
        try:
            assert 'from_address' in trx_data,'unknow from_address'
            assert 'to_address' in trx_data,'unknow to_address'
            assert 'value' in trx_data,'unknow value'
            assert trx_data['value'] < 1000 , 'invalid value'
        except AssertionError as err:
            raise CREATE_TX_ERROR(err)
        tx = Tx(trx_data['from_address'],trx_data['to_address'],trx_data['value'])
        txHash = tx.getTxHash()
        TX_POOL[txHash] = Tx
        respData = {'status':'success','txHash':txHash}
        resp = web.json_response(respData)
        return resp

'''
    Address
'''
class Address():
    def __init__(self,balance,nonce):
        self.balance = balance
        self.nonce = nonce

MINE_DIFFICULTY = 0x01* (2 ** (8*(6-3)))
TX_POOL = {}
BLOCK_CHAIN = []
GENESIS_BLOCK_HASH = '00' * 32
"""
    mine Block
"""
def mine():
    timestamp = round(time.time())
    trx = []
    print(TX_POOL,'TX_POOL')
    for k in TX_POOL:
        trx.append(k)   
    merkle_root = Tx.calc_merkle_root(trx)
    previous_block = BLOCK_CHAIN[-1]['block_hash']
    nonce = 0
    target = 2**256 / MINE_DIFFICULTY
    while (1):
        headerData = str(timestamp) \
                + merkle_root \
                + previous_block \
                + str(nonce)
        blockHash = hash_sha256(headerData.encode('utf-8'))
        if int(blockHash,16) < target:
            print('mined ' + blockHash)
            block_dict = {
                'timestamp': timestamp,
                'merkle_root':merkle_root,
                'previous_block':previous_block,
                'trx': trx,
                'nonce':nonce,
                'block_hash':blockHash
            }
            BLOCK_CHAIN.append(block_dict)
            for t in trx:
                if t in TX_POOL:
                    del TX_POOL[t]
            break;
        else:
            nonce += 1
    mine()

#
# tx_1 = Tx('0x123456789','0x987654321',100) 
# tx_2 = Tx('0x123456789','0x987654321',100) 
# tx_3 = Tx('0x123456789','0x987654321',100) 
# tx_4 = Tx('0x123456789','0x987654321',100)

def create_genesis_block():
    timestamp = time.time()
    trx = []
    merkle_root = '00' * 32
    previous_block = '0000'
    nonce = 0
    block_hash = hash_sha256((str(timestamp) \
        + merkle_root + previous_block + str(nonce)).encode('utf-8'))
    # return Block(timestamp,merkle_root,previous_block,nonce,trx,block_hash)
    block = {
        'timestamp': timestamp,
        'merkle_root':merkle_root,
        'previous_block':previous_block,
        'trx': trx,
        'nonce':nonce,
        'block_hash':block_hash
    }
    BLOCK_CHAIN.append(block)

def server():
    app = web.Application()
    app.add_routes([
        web.post('/trx/add',Tx.create_tx),
        web.get('/blockheight/{height}',Block.getBlockByHeight)
    ])
    web.run_app(app)

if __name__ == '__main__':
    create_genesis_block()
    _thread.start_new_thread(mine,())
    server()






