import numpy as np
import math 
import copy 
'''
The expectation maximization algorithm

The expectation maximization algorithm starts with a random choice of Parameters. It then alternates between the E-step, in which we compute a responsibility matrix HiddenMatrix for Data given Parameters:

(Data, ?, Parameters) → HiddenMatrix

and the M-step, in which we re-estimate Parameters using HiddenMatrix:

(Data, HiddenMatrix, ?) → Parameters

Lloyd algorithm into a soft k-means clustering algorithm. This algorithm starts from randomly chosen centers and iterates the following two steps:

Centers to Soft Clusters (E-step): After centers have been selected, assign each data point a “responsibility” value for each cluster, where higher values correspond to stronger cluster membership. 
Soft Clusters to Centers (M-step): After data points have been assigned to soft clusters, compute new centers.
'''

def main():

    def Clusters2Centers(Centers,Cntr2Dist):
        d={}
        dc={}
        DistN=0
        Sumo=0
        # Calculate Center of Gravity for each Center 
        # tuple 0=center list, tuple 1 = data point list, tuple2=Distance
        for row in Cntr2Dist:
           DistN+=1
           #print("Center=>",row[0],"Pt : ",row[1],"  Dist: %6.2f " % (row[2]))
           if tuple(row[0]) not in d:
               d[tuple(row[0])]=row[1]
               dc[tuple(row[0])]=1
           else:
               d[tuple(row[0])]=addDist(d[tuple(row[0])],row[1])
               dc[tuple(row[0])]+=1
        #print("Center of Gravity for each Center is in Dictionary d")

        for k,v in d.items():
           N=dc[k]
           newCenter=[]
           for item in v:
               newCenter.append(item/N)

           Centers=delRow(Centers,k)
           Centers = np.vstack((Centers,newCenter))
        return Centers

    def CalcDistortion(Cntr2Dist):
        d={}  ## Dictionary to accumulate Center to DataPt distance squared
        dc={} ## Dictionary to accumulate Center to its DataPt counts 
        DistN=0
        Sumo=0
        #tuple 0=centerlist, tuple 1=data point list, tuple 2 = Distance
        for row in Cntr2Dist:
           DistN+=1
           #print("Center=>",row[0],"Pt : ",row[1],"  Dist: %6.2f " % (row[2]))
           if tuple(row[0]) not in d:
               d[tuple(row[0])]=math.pow(float(row[2]),2)
               dc[tuple(row[0])]=1
           else:
               d[tuple(row[0])]+=math.pow(float(row[2]),2)
               dc[tuple(row[0])]+=1
        print("Dictionary to accumulate dimensional sum and counts loaded")
  
        for row in d:
            Sumo+=d[row]

        #This needs to be stored, Distortion per center, here its just the last 

        Distort=Sumo/DistN    

        return Distort 

    def ddelRow(Array2D,pattrn):
        print("find and remove rows that match all",pattrn)
        mp=np.where(np.all(Array2D==pattrn,axis=1))
        print("Found old center ",mp,", delete it.")

        for ii in mp:
           #print("---> remove positions ",ii)
           ix=list(ii)
           Array2D=np.delete(Array2D,ix,0)

        return Array2D

    def ClosestCenter(Data,Centerz):
        MaxD=-100.0
        MinD=100000.0
        bCntr=[]
        thisCenter=5.0
      
        for i in Data:  #  find the closest center for each datapoint
           for j in Centerz:  # store it
                xy=Edist(i,j)
                if xy < MinD :
                   MinD=xy
                   thisCenter=j
           
           #Datapoints assigned to center: Dist, Cnrt, data pt
           #print("Decided  on ",MinD," Data to Center ",i,thisCenter)
           bCntr.append((thisCenter,i,MinD))
           MinD=100000.0  # reset
        return bCntr 

    def delRow(Array2D,pattrn):
        print("find and remove rows that match all",pattrn)
        mp=np.where(np.all(Array2D==pattrn,axis=1))
        print("Found old center ",mp,", delete it.") 
    
        for ii in mp:
           #print("---> remove positions ",ii)
           ix=list(ii)
           Array2D=np.delete(Array2D,ix,0) 

        return Array2D 



    def Edist(A,B):
        '''
        Euclidean distance between two n-dimensional points.
        '''
        return np.sqrt(np.sum((A - B)**2))

    def addDist(A,B):
        # Sum the distance of two n-dimensional points.
        return np.add(A,B)

    '''
    Open hardcoded file, parse data anticipataed but may change
    Load just data into a numpy array, 
    '''
    #f = open('wk2_2.dat', 'r')
    f = open('wk2_2.dat', 'r')
    cnt=0
    Dataflag=False
    print("Loading data . . .")
    # K is used to grab the first K lines as clusters, don't consider them
    # Data at this time, that may not be correct
    for line in f:
        xx=line.rstrip() # get rid of cr
        if cnt==0:       # known line to contain only K and M
           v=xx.split(' ')
           K=int(v[0])
           M=int(v[1])
           print("Number of Centers is ",K)
           print("Dimensionality is ",M)
           ##Use K,M to Dim numpy arrays to build, delete these rows later 
           Data = np.zeros((M), dtype=np.float)
           Centers = np.zeros((M), dtype=np.float)
        elif cnt==1:
           Beta=float(xx)
           print("Beta is ",Beta)
        ## pseudo gene looks for some marker not used but may be in the future
        elif any(c in '----' for c in xx):
           print("Data time")
           Dataflag=True
        elif cnt > 1:
           ##Parse data, put rows in list, list appended to a numpy array
           w=xx.split(" ")
           new_list = []
           for item in w:
               new_list.append(float(item))
           Data = np.vstack((Data,new_list))
        else:
           print("Something is wrong, bail")

        cnt+=1
    print("Data points read: ",cnt-2)
    ### remove phoney line 0 that established shape.  Find a better way later
    Data=np.delete(Data, 0, 0)
    print("Data is ",Data)

    print("Copy first K data points into Centers")
    Centers=copy.deepcopy(Data[:K])

    print("Cleanded Centers is ")
    print(Centers)
    Done=False
    oldDistortion=50000
    coa=0
    while Done==False:
        ############################################################
        #  Map centers to data pts, keep the distance as well
        #  Returns Array of 3 part tuple, (Center Array, DataPt Array and Dist)
        #  Centers to Clusters Phase
        #  

        Center2PtDist=ClosestCenter(Data,Centers)

        #
        # extract tuples from the 3mer with additional index 
        # where first [] is row, second is the tuple 1 of 3
        print(Center2PtDist[0][0],Center2PtDist[0][1],Center2PtDist[0][2])
        #  will show row 0, tuples 1 to 3
        #exit()
        ############################################################
        #  Calculate Distortion for all clusters to determine continuation

        Distortion=CalcDistortion(Center2PtDist)
        
        #########################################

        print("Loop ",coa,"Distortion is is %5.3f " % (Distortion))
        if Distortion >= oldDistortion:
            Done=True
        else:
           oldDistortion=Distortion

        ##########################################################
        #Pick a new Center by gravity for each Center and its data pts
        #  Clusters to Centers Phase
        #
        ##########################################################

        Centers=Clusters2Centers(Centers,Center2PtDist)

        #  End Loop 
        coa+=1
        if coa > 50:
           print("Early termination fees, looop is",coa)
           exit()
    print("*******Final Centers is ****")
    print("Loop count is ",coa)
    print(Centers)

    niceCenter=[]
    for row in Centers:
       for element in row:
           print("%5.3f" % (element),end=" ") 
       print()
         
      #print("Center=>",row[0],"Pt : ",row[1],"  Dist: %6.2f " % (row[2]))
if __name__ == "__main__":
    main()
