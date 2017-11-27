import numpy as np
import random

def main():
    ######
    '''
    FarthestFirstTraversal(Data, k) 
    Centers ← the set consisting of a single randomly chosen point from Data
    while |Centers| < k 
        DataPoint ← the point in Data maximizing d(DataPoint, Centers) 
        add DataPoint to Centers 
    return Centers 
    '''
    ######
    def ClosestCenter(Data,Centerz):
        MaxD=-100.0
        MinD=100000.0
        bCntr=[]
        thisCenter=5.0
      
        for i in Data:  #  find the closest center for each datapoint
           for j in Centerz:  # store it
           #     print("Compart Data ",i,"to Center ",j)
                xy=Edist(i,j)
                if xy < MinD :
                   MinD=xy
                   thisCenter=j
           
           #Datapoints assigned to center now
           # Save distance, Center point and Data point
           #print("Decided  on ",MinD," Data to Center ",i,thisCenter)
           bCntr.append((MinD,thisCenter,i))
           MinD=100000.0
           #bCntr.append((xy,j,i))
        return bCntr 

    def Edist(A,B):
        '''
        Euclidean distance between two n-dimensional points.
        '''
        #AA=np.array(A)
        #BB=np.array(B)
        uu=np.sqrt(np.sum((A - B)**2))
        return uu 

    ##########################################################
    '''
    Open hardcoded file, parse data anticipataed but may change
    Load just data into a numpy array, 
    '''
    ##########################################################

    f = open('data9.txt', 'r')
    cnt=0
    for line in f:
        xx=line.rstrip() # get rid of cr
        if cnt==0:       # known line to contain K and M
           v=xx.split(' ')
           K=int(v[0])
           M=int(v[1])
           a = np.zeros((M), dtype=np.float)
        else:
           w=xx.split(" ")
           new_list = []
           for item in w:
               new_list.append(float(item))
           a = np.vstack((a,new_list))
        cnt+=1
    ### remove phoney line 0 that established shape.  Find a better way later
    a=np.delete(a, 0, 0)

    firstCenter=a[0]
    a=np.delete(a,a[0],0)
    Centers=np.array([firstCenter])

    Kcntr=1
    while Kcntr < K:
        newC=ClosestCenter(a,Centers)
        #print("distance, Center point and Data point")
        #for ju in newC:
        #   print(ju)
    
        qq=max(newC)    
        Kcntr+=1
        Centers = np.vstack((Centers,qq[2]))
        a=np.delete(a,qq[2],0)
    
    #print("Final Distance is ",qq[0])
    #print("Final Center is ",qq[1])
    #print("Final Data Pt is ",qq[2])

    #print("The centers are ",Centers)
    Carray=list(Centers)
    for row in Carray:
       for element in row:
          print(element,end=' ')
       print('\n')

if __name__ == "__main__":
    main()
