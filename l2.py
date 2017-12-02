import numpy as np
import math 

def main():
    ######
    '''
    '''
    ######
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

    def Edist(A,B):
        '''
        Euclidean distance between two n-dimensional points.
        '''
        return np.sqrt(np.sum((A - B)**2))

    def addDist(A,B):
        '''
        Sum the distance of two n-dimensional points.
        '''
        uu=np.add(A,B)
        return uu 

    ##########################################################
    '''
    Open hardcoded file, parse data anticipataed but may change
    Load just data into a numpy array, 
    '''
    ##########################################################

    f = open('lloyd1.dat', 'r')
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
        ## pseudo gene looks for some marker not used but may be in the future
        elif any(c in '----' for c in xx):
           print("Data time")
           Dataflag=True
        elif cnt <= K:
           w=xx.split(" ")
           temp_list=[]
           for item in w:
              temp_list.append(float(item)) 
           Centers = np.vstack((Centers,temp_list))
           #Consdier Centers as Data points as well or not
           #Data = np.vstack((Data,temp_list))
        elif cnt > K: 
           ##Parse data, put rows in list, list appended to a numpy array
           w=xx.split(" ")
           new_list = []
           for item in w:
               new_list.append(float(item))
           Data = np.vstack((Data,new_list))
        else:
           print("Something is wrong, bail")

        cnt+=1
    print("Data points read: ",cnt-K)
    ### remove phoney line 0 that established shape.  Find a better way later
    Data=np.delete(Data, 0, 0)
    Centers=np.delete(Centers, 0, 0)
    Done=False
    oldDistortion=500
    coa=0
    while Done==False:
        ############################################################
        #    Map centers to data pts, keep the distance as well

        ss=ClosestCenter(Data,Centers)

        ############################################################
        '''
        Calculate Distortion for all clusters
        '''
        d={}
        dc={}
        DistN=0
        Sumo=0
        # Calculate Total Distortion
        #tuple 0=centerlist, tuple 1=data point list, tuple 2 = Distance
        for row in ss:
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
            #print("Final answer ",float(d[row])/float(dc[row]))
            Sumo+=d[row]
        #This needs to be stored, Distortion per center, here its just the last 
        Distortion=Sumo/DistN    
        print("Distortion is is %5.3f " % (Distortion))
        if Distortion >= oldDistortion:
            Done=True
        else:
           oldDistortion=Distortion

        ############################################################
        '''
        Pick a new Center by gravity for each Center and its data pts
        '''
        d={}
        dc={}
        DistN=0
        Sumo=0
        # Calculate Center of Gravity for each Center 
        # tuple 0=center list, tuple 1 = data point list, tuple2=Distance
        for row in ss:
           DistN+=1
           #print("Center=>",row[0],"Pt : ",row[1],"  Dist: %6.2f " % (row[2]))
           if tuple(row[0]) not in d:
               d[tuple(row[0])]=row[1]
               dc[tuple(row[0])]=1
           else:
               d[tuple(row[0])]=addDist(d[tuple(row[0])],row[1])
               dc[tuple(row[0])]+=1
        print("Dictionary loaded")
        print(d) 
        print(dc)
        print("--------------------")
        for k,v in d.items():
           print("Center is ",k)
           print("Summed distance array is", v)
           print("N is ",dc[k])
           N=dc[k]
           newCenter=[]
           for item in v:
               newCenter.append(item/N)
        print("newCenter is ",newCenter)   

        print("Before add to centers",Centers)
        Centers = np.vstack((Centers,newCenter))
        print("After new add to Centers ", Centers)
        print("remove ",k)
        mp=np.where(np.all(Centers==k,axis=1))
        print("Found ",mp," to delete") 
        for ii in mp:
           for jj in ii:
               print("Find it in ",int(jj))
           Centers=np.delete(Centers,int(jj),axis=0) 

        print("************")
        print("************")

        print("Final Centers is now ", Centers)
        coa+=1
    print("Final Centers is ", Centers)
    print("Final System is ",ss)
if __name__ == "__main__":
    main()
