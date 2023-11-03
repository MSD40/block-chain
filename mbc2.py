import hashlib

class merkle_tree:
    def __init__ (self,*args): 

        #converting tuple to a list
        listargs=list(args[:])
       
        i=0
        
        #hashing the objects
        while(i<len(args)):
            hash_i = hashlib.sha256(str((args[i])).encode()).hexdigest()
            listargs.pop(i)
            listargs.insert(i,hash_i)
            # print(listargs[i])
            i += 1
        
        hash_list=[]
        var_list=[]
        # print(listargs)
        if(len(listargs)!=1):
            while(i!=-1): 
                if(len(listargs)%2==0):
                    var=int(len(listargs)/2)
                    i=0

                    while(i<var and i>-1):

                        #sum of 2 leaf 
                        new_hash=listargs[0]+listargs[1]
                        # new_hash=hex(int(listargs[0], 16)+int(listargs[1], 16))
                        # print(f"sum_hash : {new_hash}")
                        #hash of the sum
                        new_hash=hashlib.sha256(str((new_hash)).encode()).hexdigest()
                        # print(f"new_hash : {new_hash}")
                        var_list.append(listargs[0])
                        var_list.append(listargs[1])
                        listargs.pop(1)
                        listargs.pop(0)
                        listargs.append(new_hash)
                        i +=1
                        if(len(listargs)==1):
                            hash_list.append(var_list)
                            var_list=listargs
                            # print("merkle :")
                            # print(f"hash list={hash_list}")
                            i=-1
                            break
                            
                    hash_list.append(var_list)
                    var_list=[]  
                else: listargs.append(listargs[len(listargs)-1])
                self.merkle=listargs[0]
                self.hash_list=hash_list
            
    
        else:    
    #  print("merkle :")
          self.merkle=listargs[0]
          self.hash_list=[listargs]


    def search(self,n):
        n = hashlib.sha256(str((n)).encode()).hexdigest()
        i=0
        j=0
        while(i<len(self.hash_list[0])):
            if(n == self.hash_list[0][i]):
                # print(self.hash_list[0][i])
                # print(f"the tx is in the tx list . in index [{0}] [{i}]")
                j=1
            i+=1
        if(j!=1):
            # print("tx in not in the tx list !")
            return False
        else :
            return True
         



                
               


      
    
# NoTX=int(input("pls enter the number of transactions : "))
# # NoTX : number of transactions
# txlist=[]
# for i in range(0,NoTX) :
#     var=str(input("enter the transactions :"))
#     txlist.append(var)
# a = merkle_tree()
# print(a.hash_list)
# print(a.merkle)
# var=input("enter the intended tx to check if it's in the list : ")
# print(a.search(var))
# data=["1"]

# print(merkle_tree(*data).merkle)