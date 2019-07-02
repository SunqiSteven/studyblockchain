
import hashlib
import time
import json
import requests
import argparse
import _thread
import socket

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
    @classmethod
    def calc_merkle_root(cls,trx):
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
            tx_data = json.loads(data.decode('utf-8'))
        except:
            return web.json_response({'status':"fail",'msg':'params format error'})
        try:
            assert 'sig' in tx_data, 'unknow sig'
            assert 'from_address' in tx_data,'unknow from_address'
            assert 'to_address' in tx_data,'unknow to_address'
            assert 'value' in tx_data,'unknow value'
            assert tx_data['value'] < 1000 , 'invalid value'
            assert 'timestamp' in tx_data, 'unknow timestamp'
        except AssertionError as err:
            raise CREATE_TX_ERROR(err)
        tx_str = ''
        for key in tx_data:
            tx_str += str(tx_data[key])
        tx_hash = hash_sha256(tx_str.encode('utf-8'))
        tx_data['tx_hash'] = tx_hash
        TX_POOL.append(tx_data)
        respData = {'status':'success','txHash':tx_hash}
        resp = web.json_response(respData)
        return resp

'''
    Address
'''
class Address():
    def __init__(self,balance,nonce):
        self.balance = balance
        self.nonce = nonce

MINE_DIFFICULTY = 2**20
TX_POOL = []
BLOCK_CHAIN = []
GENESIS_BLOCK_HASH = '00' * 32
PEER_LIST = []
__VERSION__ = 'v1.0.0'
SERVER_PORT = '8084'
"""
    peer 
"""
class Peer():
    def __init__(self):
        pass
    @classmethod
    async def version(cls,request):
        data = {'version':__VERSION__}
        resp = web.json_response(data)
        return resp
    @classmethod
    async def getPeerList(cls,request):
        return web.json_response(PEER_LIST)
    @classmethod
    async def addr(cls,request):
        data = await request.content.read()
        try:
            body = json.loads(data)
        except:
            return web.json_response({'status':'fail','msg':'invalid data'})
        try:
            assert 'host' in body, 'host not exists'
            assert 'port' in body, 'port not exists'
        except AsssertionError as err:
            return web.json_response({'status':'fail','msg':err.value})
        body['status'] = 1
        PEER_LIST.append(body)
        return web.json_response({'status':'success'})
"""
    mine Block
"""
def mine():
    timestamp = round(time.time())
    trx = []
    print(TX_POOL,'TX_POOL')
    tx_pool_len = len(TX_POOL)
    for index in range(tx_pool_len):
        trx.append(TX_POOL[index]['tx_hash'])  
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
######
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
######
def check_peer_list():
    while 1:
        time.sleep(60)
        for i in range(len(PEER_LIST)):
            peer = PEER_LIST[i]
            r = requests.get('http' + '://' +peer['host'] + ':' + str(peer['port']))
            if r.status_code != 200:
                PEER_LIST.pop(i)
                # peer['status'] = 0
###
def createConnect(peer):
    try:
        r = requests.get('http://'+ peer + '/version')
        if r.status_code == 200:
            host_port = peer.split(':',1)
            p = {'host':host_port[0],'port':host_port[1],'status':1}
            PEER_LIST.append(p)
            ip = get_host_ip()
            data = {'host':ip,'port':SERVER_PORT}
            url = 'http://'+ peer + '/addr'
            # print('addr')
            r = requests.post(url,data=json.dumps(data))
            # print(r.text)
    except:
        pass
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

def server(port):
    app = web.Application()
    app.add_routes([
        web.post('/trx/add',Tx.create_tx),
        web.get('/blockheight/{height}',Block.getBlockByHeight),
        web.get('/peers',Peer.getPeerList),
        web.get('/version',Peer.version),
        web.post('/addr',Peer.addr),
    ])
    # host = get_host_ip()
    web.run_app(app,port=port)

if __name__ == '__main__':
    cmdParser = argparse.ArgumentParser()
    cmdParser.add_argument('--peer',help='connect to peer')
    cmdParser.add_argument('--port',help='server listen port',default=SERVER_PORT)
    args = cmdParser.parse_args()
    if args.peer:
        createConnect(args.peer)
    #   
    create_genesis_block()
    #
    _thread.start_new_thread(mine,())
    #
    _thread.start_new_thread(check_peer_list,())
    #
    SERVER_PORT = args.port
    server(SERVER_PORT)






