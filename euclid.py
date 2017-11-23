import numpy as np
import random

###
def Edist(A,B):
    return np.sqrt(np.sum((A - B)**2))

f = open('data2.txt', 'r')
cnt=0
data=False
answer=False
a = np.array([1,2,3,4,5])
for line in f:
    xx=line.rstrip() # get rid of cr
    if cnt==1:       # known line to contain K and M
       v=xx.split(' ')
       K=v[0]
       M=int(v[1])
       print('K is ',K)
       print('M is ',M)
    elif xx=='Input':
       data=True
       print('Found Input Tag')
    elif xx=='Output':
       answer=True
       data=False 
       print('Found Output Tag')
    else:
       if data==True:
           w=xx.split(" ")
           new_list = []
           for item in w:
               new_list.append(float(item))
           print('adding ',new_list)
           a = np.vstack((a,new_list))

       if answer==True:
           x=xx
           print(':',x)
    cnt+=1
a=np.delete(a, 0, 0)
for i in a:
        print(i)

#print(a.shape)
#row=random.randint(1, cnt)
#col=random.randint(0, 4)
#print('Here is row',row,"  col ",col)
#print(a[row][col])
print('vector 1 is ',a[0])
print('vector 2 is ',a[1])
x = Edist(a[0],a[1])
print(x)
###   We have now loaded a numpy array and will select a row, the first
###   or a random row, to be a starting point and compare it to all the other
###   points in the array and take the largest.
###   Distance is d(v,w) = sqrt(sum((v-w)**2))


