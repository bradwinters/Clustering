import numpy as np

f = open('data2.txt', 'r')
cnt=0
data=False
answer=False
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
           print('->',new_list)
           print('new_list type is ',type(new_list))
           for point in new_list:
               print(point)
       if answer==True:
           x=xx
           print(':',x)
    cnt+=1
