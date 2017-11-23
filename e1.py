import numpy as np
import random

###
###   Distance is Edist(V,W) = sqrt((sum((v-w)**2))
def Edist(A,B):
    return np.sqrt(np.sum((A - B)**2))

def MaxDistance(Data,Centerz):
     Max=-1.0
     print("****  Centerz is ****")
     print(Centerz)
     print("****  Data is ****")
     print(Data)
     for eachCenter in Centerz: 
         print("on pair ",eachCenter)
         for eachPair in Data:
             x = Edist(eachCenter,eachPair)
             print("Dist between ",eachCenter," ",eachPair," is ",x)
             if x > Max:
                 Max=x
     print("****  Done wih function ****")
     return Max

## data file has k and M in line 0 followed by vectors of M dimensions
f = open('test.dat', 'r')
cnt=0

## Given the following this time, may have to generate these from datafile
Centers=np.array([[2,4],[6,7],[7,3]])
a = np.array([1,2])
for line in f:
    xx=line.rstrip() # get rid of cr
    if cnt==0:       # known line to contain K and M
       v=xx.split(' ')
       K=v[0]
       M=int(v[1])
       print('K is ',K)
       print('M is ',M)
    else:
       w=xx.split(" ")
       new_list = []
       for item in w:
           new_list.append(float(item))
       print('adding ',new_list)
       a = np.vstack((a,new_list))

    cnt+=1
a=np.delete(a, 0, 0)
for i in a:
        print(i)

#row=random.randint(1, cnt)
#col=random.randint(0, 4)
x = Edist(a[0],a[1])
print(x)
print("Centers is ",Centers)
###   We have now loaded a numpy array and given Centers will find maxDistance
###   Call MaxDistance(Data, Centers) 

answ=MaxDistance(a,Centers)
print("Max Distance is ",answ)
