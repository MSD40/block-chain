import datetime
import hashlib
from flask import Flask, jsonify
from mbc2 import merkle_tree
import time

# Genesis Block defined
class Blockchain:
   def __init__(self):
       self.chain = []
       self.create_blockchain(proof=1, previous_hash='0')
# Blocks are defined  
   def create_blockchain(self, proof, previous_hash,*data):
       block = {
           'index': len(self.chain) + 1,
           'timestamp': str(datetime.datetime.now()),
           'proof': proof,
           'previous_hash': previous_hash ,
           'data': data
       }

       self.chain.append(block)
       return block

   def get_previous_block(self):
       last_block = self.chain[-1]
       return last_block

   def proof_of_work(self, previous_hash,difficulty=4):
# Miners proof or nonce
       new_proof = 1
       check_proof = False
       while check_proof is False:
             nonce = hashlib.sha256(str(new_proof).encode()).hexdigest()
             hash_operation = hashlib.sha256(str(nonce + previous_hash).encode()).hexdigest()
# Proof results in X leading zero's in the hash operation

             var=1
             zeros_in_difficulty=str(0)
             while(var<difficulty):
                zeros_in_difficulty += str(0)
                var+=1
             if hash_operation[:difficulty] == zeros_in_difficulty:
                    self.zeros_in_difficulty = zeros_in_difficulty
                    self.difficulty=difficulty
                    check_proof = True
             else:
# If miners solution is wrong, add one until correct
                    new_proof += 1
       return new_proof
   
        
     

# Generate the hash of the entire block
   def hash(self, block,*data):

    ###    encoded_block = json.dumps(block, sort_keys=True).encode()
       body_header_hash= str(block) + merkle_tree(data).merkle
       return hashlib.sha256((body_header_hash).encode()).hexdigest()

   # check if the blockchain is valid
   def is_chain_valid(self, chain):
       # get the first block in the chain and it serves as the previous block
       previous_block = chain[0]
       previous_data=previous_block['data']
       # an index of the blocks in the chain for iteration
       block_index = 1
       while block_index < len(chain):
           # get the current block
           block = chain[block_index]
           # check if the current block link to previous block has is the same as the hash of the previous block
           if block["previous_hash"] != self.hash(previous_block,*previous_data):
               return False

           # get the previous proof from the previous block
           previous_hash = block['previous_hash']

           # get the current proof from the current block
           current_proof = block['proof']

           # run the proof data through the algorithm
           hash_operation = hashlib.sha256(str(hashlib.sha256(str(current_proof).encode()).hexdigest() + previous_hash).encode()).hexdigest()
           # check if hash operation is invalid
           if hash_operation[:self.difficulty] != self.zeros_in_difficulty:
               return False
           # set the previous block to the current block after running validation on current block
           previous_block = block
           block_index += 1
       return True


      



app = Flask(__name__)

blockchain = Blockchain()
var1=input(str("do you want to change the difficulty ? (y/n)    (default is 4) "))
if var1 == 'y':
    difficulty=int(input("enter the intended difficulty : "))
else: 
    difficulty=4
    

@app.route('/mine_block', methods=['GET'])
def mine_block():
    
# Get the data we needed to create a block
    NoTX=int(input("pls enter the number of transactions : "))
            # NoTX : number of transactions
    data=[]
    for i in range(0,NoTX) :
            var=str(input("enter the transactions :"))
            data.append(var)
    start=time.time()
    previous_block = blockchain.get_previous_block() 

   
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_hash,difficulty)
    block = blockchain.create_blockchain(proof, previous_hash,*data)
    response = {'message': 'Block mined!',
               'index': block['index'],
               'timestamp': block['timestamp'],
               'proof': block['proof'],
               'previous_hash': block['previous_hash']}
    end=time.time()
    run_time=end-start
    print("The time of execution of above program is :",
      (run_time), "s")
    return jsonify(response,run_time), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
   response = {'chain': blockchain.chain}
   i=0     
   chain=[]
   for i in response.values():
        for j in i:
            # print(j)
            chain.append(j)    

   return jsonify(response,blockchain.is_chain_valid(chain)), 200

app.run(host='0.0.0.0', port=5000)