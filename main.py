import gmpy2
from gmpy2 import mpz
class sender:
    #initializing parameters
    def __init__(self,prime,prim_root,random_state):
        self.p=mpz(prime)
        self.g=mpz(prim_root)
        self.k1=gmpy2.mpz_random(random_state,p)
        self.x1=gmpy2.powmod(self.g,self.k1,self.p)
        
    
    #returns g^k1(modp)    
    def key(self):
        return self.x1
    
    #common section key
    def c_s_k(self,x2):
        self.x21=gmpy2.powmod(x2,self.k1,self.p)
        if(gmpy2.is_even(self.x21)):
            self.e=gmpy2.sub(self.x21,1)
        else:
            self.e=self.x21
        self.d=gmpy2.divm(1,self.e,gmpy2.sub(p,1))
        return self.x21
        
    
    def common_key(self):
        return self.e
    
    def inverse(self):
        return self.d    
            
    #retuns encrypted message
    def encrypt(self,str):
        l=len(str)
        #print(l)
        m=mpz(0)
        for i in range(0,l):
            #print(i)
            if(ord(str[l-1-i])==32):
                m+=27*(29**i)
            elif(ord(str[l-1-i])==46):
                m+=26*(29**i)
            elif(ord(str[l-1-i])==63):
                m+=28*(29**i)
            elif(65<=ord(str[l-1-i])<=90):
                temp=ord(str[l-1-i])-65
                m+=temp*(29**i)
        c=gmpy2.powmod(m,self.e,self.p)
        #print(m,"  ",c)
        encrypted=""
        for i in range(0,l+1):
            t1=gmpy2.f_mod(c,29**(l-i))
            temp=gmpy2.f_div(c,29**(l-i))
            c=t1
            if(0<=temp<=25):
                encrypted+=chr(temp+65)
            elif(temp==26):
                encrypted+="."
            elif(temp==27):
                encrypted+=" "
            elif(temp==28):
                encrypted+="?"               
        return encrypted
        #return gmpy2.powmod(m,self.e,self.p)
    


class receiver:
    #initializing parameters
    def __init__(self,prime,prim_root,random_state):
        self.p=mpz(prime)
        self.g=mpz(prim_root)
        self.k2=gmpy2.mpz_random(random_state,p)
        #print(self.k2)
    #returns g^k1(modp)    
    def key(self):
        return gmpy2.powmod(self.g,self.k2,self.p)
    
    #common section key
    def c_s_k(self,x1):
        self.x12=gmpy2.powmod(x1,self.k2,self.p)
        if(gmpy2.is_even(self.x12)):
            self.e=gmpy2.sub(self.x12,1)
        else:
            self.e=self.x12
        self.d=gmpy2.divm(1,self.e,self.p-1)
        return self.x12
        #print(self.d," ","user2")
    #inverse of e
    
    def common_key(self):
        return self.e
    
    def inverse(self):
        return self.d
    #returns decrypted message
    def decrypt(self,str):
        l=len(str)
        #print(l)
        m=mpz(0)
        for i in range(0,l):
            #print(i)
            if(ord(str[l-1-i])==32):
                m+=27*(29**i)
            elif(ord(str[l-1-i])==46):
                m+=26*(29**i)
            elif(ord(str[l-1-i])==63):
                m+=28*(29**i)
            elif(65<=ord(str[l-1-i])<=90):
                temp=ord(str[l-1-i])-65
                m+=temp*(29**i)
        c=gmpy2.powmod(m,self.d,self.p)
        #print(m,"  ",c)
        encrypted=""
        for i in range(0,l-1):
            t1=gmpy2.f_mod(c,29**(l-2-i))
            temp=gmpy2.f_div(c,29**(l-2-i))
            #print(c," ",t1," ",temp," ",l)
            c=t1
            
            if(0<=temp<=25):
                encrypted+=chr(temp+65)
            elif(temp==26):
                encrypted+="."
            elif(temp==27):
                encrypted+=" "
            elif(temp==28):
                encrypted+="?"
               
        return encrypted

#print(gmpy2.f_div(5,3))
file1=open("input","r")
file2=open("output_pre_generated","w")
file3=open("output","w")
message=file1.readline()
p=mpz(file1.readline())
g=mpz(file1.readline())
file3.write("the message user1 wants to send to user2 :  \n")
file3.write(message)
file3.write("\n")
file3.write("\n")
#p= mpz(input("enter the prime p :"))
#g=mpz(input("enter primetive root of p :"))
#message=input("enter the message to be encrypted :")
n=mpz(len(message))
n=n-1
message=message[0:n]
#print(message)
b=mpz()
random_state=gmpy2.random_state()
User1=sender(p,g,random_state)
User2=receiver(p,g,random_state)
x1=User1.key()
x2=User2.key()
x21=User1.c_s_k(x2)
x12=User2.c_s_k(x1)
e1=User1.common_key()
d1=User1.inverse()
e2=User2.common_key()
d2=User2.inverse()
file2.write("info of sender :\n")
l1=["x1 : ",str(x1),"\n","x12 : ",str(x21),"\n","e : ",str(e1),"\n","d : ",str(d1),"\n"]
file2.writelines(l1)
file2.write("info of reciver :\n")
l2=["x2 : ",str(x2),"\n","x21 : ",str(x12),"\n","e : ",str(e2),"\n","d : ",str(d2)]
file2.writelines(l2)
for i in range (1,n):
    if(mpz(29)**i >p):
        b=i-1
        break
#end of loop
r=gmpy2.f_mod(n,b)
for i in range(0,r):
    message+=" "
#loop ended
q=gmpy2.c_div(n,b)
encrypt_message=""
for i in range (0,q):
    str=message[i*b:(i+1)*b]
    encrypt_message+=User1.encrypt(str)
#end of loop
l1=["the encrypted message is :","\n", encrypt_message,"\n"]
file3.writelines(l1)
file3.write("\n")
b=b+1
decrypt_message=""
for i in range (0,q):
    str=encrypt_message[i*b:(i+1)*b]
    decrypt_message+=User2.decrypt(str)    
l2=["the decrypted message is :","\n", decrypt_message]    
file3.writelines(l2)
file1.close()
file2.close()
file3.close()