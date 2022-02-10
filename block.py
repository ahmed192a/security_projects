from hashlib import sha256
from random import randint
import json
import time
import math

#############################################################################################################
class Users:
    def __init__(self,name):
        self.name=name
        
    def make_block(self,blockchain):
        block=Block(index=blockchain.last_block.index + 1, 
                       transactions=blockchain.unconfirmed_transactions,
                       time_stamp=time.time(),
                       prev_hash=blockchain.last_block.hash,
                       nonce=64)
        return block
    
    def mining(self,block,blockchain):     
        proof=blockchain.mine(block)
        return proof
    
    def attack(self):
        block=Block(index=generalblockchain.last_block.index, 
                        transactions=generalblockchain.unconfirmed_transactions,
                        time_stamp=time.time(),
                        prev_hash=generalblockchain.chain[-2].hash, #hash of the block before the last verified block#
                        nonce=64)
        return block
        
       
class Block:
    def __init__(self,index,transactions,time_stamp,prev_hash,nonce):
        self.index=index
        self.transactions=transactions
        self.time_stamp=time_stamp
        self.prev_hash=prev_hash
        self.nonce=nonce
        
    def compute_hash(self):
        block_string=json.dumps(self.__dict__,sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
    
class BlockChain:
    def __init__(self):
        self.unconfirmed_transactions = []
        #creating the chain that keeps track of the blocks 
        self.chain=[]
        #creating the initial block
        self.create_genesis_block()
     
    #initialize the block_chain
    #creates an initial block with index 0 and prev_hash of 0
    def create_genesis_block(self):
        genesis_block = Block(0,[],time.time(),"0",64)
        genesis_block.hash = genesis_block.compute_hash()
        #add the initial block to the chain
        self.chain.append(genesis_block)
        
    @property
    def last_block(self):
        return self.chain[-1]
    
    difficulty=3
    
    def proof_of_work(self,block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * BlockChain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def add_block(self,block,proof):
        prev_hash=self.last_block.hash
        if not self.is_valid_proof(block,proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self,block,block_hash):
        return (block_hash.startswith('0' * BlockChain.difficulty) and block_hash == block.compute_hash())
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transaction.append(transaction)
        
    def mine(self,block):
        proof=self.proof_of_work(block)
        return proof

        
def get_chain(blockchain):
    chain_data=[]
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data), "chain": chain_data})  
#########################################################################################   
#making a blockchain of length 3 blocks 
generalblockchain = BlockChain()

print("Difficulty is 4 \n\n")
print("The Block Chain Information :", get_chain(generalblockchain),"\n\n")




#creating users for simulating the system
userA = Users("A")
userB = Users("B")

#create identical blocks for these users 
blockA=userA.make_block(generalblockchain)
time1=time.time()
proofA=userA.mining(blockA,generalblockchain)
time2=time.time()
timeA=time2-time1
generalblockchain.add_block(blockA,proofA)
print("User A Added a block to the BlockChain")
print("Time required to add a block = ",math.ceil(timeA),"Sec\n\n")

blockB=userB.make_block(generalblockchain) 
time1=time.time()
proofB=userB.mining(blockB,generalblockchain)
time2=time.time()
timeB=time2-time1
generalblockchain.add_block(blockB,proofB)
print("User B Added a block to the BlockChain")
print("Time required to add a block = ",math.ceil(timeB),"Sec\n\n")
    
print("The Block Chain information :",get_chain(generalblockchain),"\n")
###########################################################################################
print("*****Simulation of the Attack if the Attacker has 25% of the computational power:*******\n")

attacker=Users("X") #the attacker#
blockx=attacker.attack()
proofx=attacker.mining(blockx,generalblockchain)
generalblockchain.add_block(blockx,proofx)
print("The Block Chain information after adding the attacker block:",get_chain(generalblockchain),"\n")
print("*The Attacker block is added to the block before the last verified block*\n")
attacker_branch = BlockChain()
attacker_branch.chain[0]=generalblockchain.chain[-1]
normal_nodes_branch = BlockChain()
normal_nodes_branch.chain[0]=generalblockchain.chain[-2]

j=0
for j in range(100):
    if(randint(0,100)%100<25):
        #attacker turn
        blockx=attacker.make_block(attacker_branch)
        proofx=attacker.mining(blockx,attacker_branch)
        attacker_branch.add_block(blockx,proofx)
    else:
        #normal nodes turn
        blockA=userA.make_block(normal_nodes_branch)
        proofA=userA.mining(blockA,normal_nodes_branch)     
        normal_nodes_branch.add_block(blockA,proofA)
        

print("Lenghth of the normal nodes branch: ",len(normal_nodes_branch.chain)-1)
print("Length of the attacker branch: ",len(attacker_branch.chain)-1)

if len(normal_nodes_branch.chain)>len(attacker_branch.chain):
    print("Attack Failed")
    del generalblockchain.chain[-1]
    print("The Attacker block is removed from the chain")
    del normal_nodes_branch.chain[0]
    generalblockchain.chain=generalblockchain.chain+normal_nodes_branch.chain
    print("The length of the Block Chain after removing the attacker branch:",len(generalblockchain.chain))
elif len(attacker_branch.chain)>len(normal_nodes_branch.chain):
    print("Attack successeded")
    print("The Last verified block is removed from the chain and the Attacker branch took its place")
    del generalblockchain.chain[-2]
    del attacker_branch.chain[0]
    generalblockchain.chain=generalblockchain.chain+attacker_branch.chain
    print("The length of the Block Chain after removing the last verified block:",len(generalblockchain.chain))
elif len(attacker_branch.chain)==len(normal_nodes_branch.chain): 
    print("Lenghtes of the branches are equal::continue minning till one of them be longer")
    while len(attacker_branch.chain)==len(normal_nodes_branch.chain):
        j=0
        for j in range(100):
            if(randint(0,100)%100<25):
                #attacker turn
                blockx=attacker.make_block(attacker_branch)
                proofx=attacker.mining(blockx,attacker_branch)
                attacker_branch.add_block(blockx,proofx)
            else:
                #normal nodes turn
                blockA=userA.make_block(normal_nodes_branch)
                proofA=userA.mining(blockA,normal_nodes_branch)     
                normal_nodes_branch.add_block(blockA,proofA)
    print("Lenghth of the normal nodes branch: ",len(normal_nodes_branch.chain)-1)
    print("Length of the attacker branch: ",len(attacker_branch.chain)-1)
    if len(normal_nodes_branch.chain)>len(attacker_branch.chain):
        print("Attack Failed")
        del generalblockchain.chain[-1]
        print("The Attacker block is removed from the chain")
        del normal_nodes_branch.chain[0]
        generalblockchain.chain=generalblockchain.chain+normal_nodes_branch.chain
        print("The length of the Block Chain after removing the attacker branch:",len(generalblockchain.chain))
    elif len(attacker_branch.chain)>len(normal_nodes_branch.chain):
        print("Attack successeded")
        print("The Last verified block is removed from the chain and the Attacker branch took its place")
        del generalblockchain.chain[-2]
        del attacker_branch.chain[0]
        generalblockchain.chain=generalblockchain.chain+attacker_branch.chain
        print("The length of the Block Chain after removing the last verified block:",len(generalblockchain.chain))

    
###################################################################################################################
print("\n")
print("****Simulation of the Attack if the Attacker has more than 50% of the computational power:*****\n")

attacker=Users("X") #the attacker#
blockx=attacker.attack()
proofx=attacker.mining(blockx,generalblockchain)
generalblockchain.add_block(blockx,proofx)
print("The lenght of the Block Chain information after adding the attacker block:",len(generalblockchain.chain),"\n")
print("*The Attacker block is added to the block before the last verified block*\n")
attacker_branch = BlockChain()
attacker_branch.chain[0]=generalblockchain.chain[-1]
normal_nodes_branch = BlockChain()
normal_nodes_branch.chain[0]=generalblockchain.chain[-2]

j=0
for j in range(100):
    if(randint(0,100)%100<60):
        #attacker turn
        blockx=attacker.make_block(attacker_branch)
        proofx=attacker.mining(blockx,attacker_branch)
        attacker_branch.add_block(blockx,proofx)
    else:
        #normal nodes turn
        blockA=userA.make_block(normal_nodes_branch)
        proofA=userA.mining(blockA,normal_nodes_branch)     
        normal_nodes_branch.add_block(blockA,proofA)
        

print("Lenghth of the normal nodes branch: ",len(normal_nodes_branch.chain)-1)
print("Length of the attacker branch: ",len(attacker_branch.chain)-1)

if len(normal_nodes_branch.chain)>len(attacker_branch.chain):
    print("Attack Failed")
    del generalblockchain.chain[-1]
    print("The Attacker block is removed from the chain")
    del normal_nodes_branch.chain[0]
    generalblockchain.chain=generalblockchain.chain+normal_nodes_branch.chain
    print("The length of the Block Chain after removing the attacker branch:",len(generalblockchain.chain))
elif len(attacker_branch.chain)>len(normal_nodes_branch.chain):
    print("Attack successeded")
    print("The Last verified block is removed from the chain and the Attacker branch took its place")
    del generalblockchain.chain[-2]
    del attacker_branch.chain[0]
    generalblockchain.chain=generalblockchain.chain+attacker_branch.chain
    print("The length of the Block Chain after removing the last verified block:",len(generalblockchain.chain))
elif len(attacker_branch.chain)==len(normal_nodes_branch.chain): 
    print("Lenghtes of the branches are equal::continue minning till one of them be longer")
    while len(attacker_branch.chain)==len(normal_nodes_branch.chain):
        j=0
        for j in range(100):
            if(randint(0,100)%100<60):
                #attacker turn
                blockx=attacker.make_block(attacker_branch)
                proofx=attacker.mining(blockx,attacker_branch)
                attacker_branch.add_block(blockx,proofx)
            else:
                #normal nodes turn
                blockA=userA.make_block(normal_nodes_branch)
                proofA=userA.mining(blockA,normal_nodes_branch)     
                normal_nodes_branch.add_block(blockA,proofA)
    print("Lenghth of the normal nodes branch: ",len(normal_nodes_branch.chain)-1)
    print("Length of the attacker branch: ",len(attacker_branch.chain)-1)
    if len(normal_nodes_branch.chain)>len(attacker_branch.chain):
        print("Attack Failed")
        del generalblockchain.chain[-1]
        print("The Attacker block is removed from the chain")
        del normal_nodes_branch.chain[0]
        generalblockchain.chain=generalblockchain.chain+normal_nodes_branch.chain
        print("The length of the Block Chain after removing the attacker branch:",len(generalblockchain.chain))
    elif len(attacker_branch.chain)>len(normal_nodes_branch.chain):
        print("Attack successeded")
        print("The Last verified block is removed from the chain and the Attacker branch took its place")
        del generalblockchain.chain[-2]
        del attacker_branch.chain[0]
        generalblockchain.chain=generalblockchain.chain+attacker_branch.chain
        print("The length of the Block Chain after removing the last verified block:",len(generalblockchain.chain))