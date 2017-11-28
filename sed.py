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
           bCntr.append((thisCenter,i,MinD))
           MinD=100000.0
           #bCntr.append((xy,j,i))
        return bCntr 

    def Edist(A,B):
        '''
        Euclidean distance between two n-dimensional points.
        '''
        uu=np.sqrt(np.sum((A - B)**2))
        return uu 

    ##########################################################
    '''
    Open hardcoded file, parse data anticipataed but may change
    Load just data into a numpy array, 
    '''
    ##########################################################

    f = open('tdata.dat', 'r')
    cnt=0
    Dataflag=False
    print("Loading data . . .")
    for line in f:
        xx=line.rstrip() # get rid of cr
        if cnt==0:       # known line to contain K and M
           v=xx.split(' ')
           K=int(v[0])
           M=int(v[1])
           print("Number of Centers is ",K)
           print("Dimensionality is ",M)
           Data = np.zeros((M), dtype=np.float)
           Centers = np.zeros((M), dtype=np.float)
        elif any(c in '----' for c in xx):
           print("Data time")
           Dataflag=True
        elif Dataflag==False:
           w=xx.split(" ")
           temp_list=[]
           for item in w:
              temp_list.append(float(item)) 
           Centers = np.vstack((Centers,temp_list))
        elif Dataflag==True:
           ##  Parse data and put rows in a list, then list is appended to a numpy array
           w=xx.split(" ")
           new_list = []
           for item in w:
               new_list.append(float(item))
           Data = np.vstack((Data,new_list))
        else:
           print("Something is wrong, bail")
        

        cnt+=1
    ### remove phoney line 0 that established shape.  Find a better way later
    Data=np.delete(Data, 0, 0)
    Centers=np.delete(Centers, 0, 0)
    print("Heres the Centers ")
    print(Centers)
    
    print("Heres the Data")
    print(Data)

    ss=ClosestCenter(Data,Centers)
    print("==============")

    d={}
    for row in ss:
       print("Center=>",row[0],"Pt : ",row[1],"  Dist: %6.2f " % (row[2]))
        
       if tuple(row[0]) not in d:
           d[tuple(row[0])]=float(row[2])
       else:
           d[tuple(row[0])]+=float(row[2])
    print("==============")
  
    for row in d:
        print(row, d[row]) 

    print("+++++++++++++++++++++++++++++") 
    planets=list(ss)
    for row in planets:
       for element in row:
          print(element,end=' ')
       print('\n')

    #sed=Distortion(a,Centers)
    x=50.02233433
    print("Number: %4.2f " % (x)) 

    exit() 

if __name__ == "__main__":
    main()
