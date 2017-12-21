import numpy as np
import math 
import copy 
from random import randint
'''
'''

def AveDist(row1,row2,Width):

    AvgdRow=[] 
    for pt in range(Width): 
       if (row1[pt]==0.0 or row2[pt] == 0.0):
          element=0 
       else:
          element=(row1[pt]+row2[pt])/2.0

       AvgdRow.append(element)

    return AvgdRow


def MinPos(pData):
    
    LowestV=10000000
    for i in range(len(pData)):
        for j in range(len(pData)):
            if pData[i][j] < LowestV and pData[i][j] > 0.0: 
                LowestV=pData[i][j]  
                XyPos=(i,j)

    return LowestV, XyPos 


class ParameterClass:
    K=0
    M=0
    Beta=0

def readData():
    '''
    Open hardcoded file, parse data anticipataed but may change
    Load just data into a numpy array, 
    '''
    #f = open('book.dat', 'r')   #Smaller dataset 
    #f = open('wk2_2.dat', 'r')  #Larger test dataset 
    f = open('data1.dat', 'r')   #Smaller dataset 
    #f = open('data2.dat', 'r')   #Smaller dataset 
    cnt=0
    dataCnt=0
    clist=[] # list of centers, initially one per data point
    lookupC={} # dict to track position of combined centers 
    print("Loading data . . .")
    # K is used to grab the first K lines as clusters, don't consider them
    # Data at this time, that may not be correct
    for line in f:
        xx=line.rstrip() # get rid of cr
        if cnt==0:       # known line to contain only K and M
           n=int(xx)
           ##Use n, to Dim numpy array to build, delete row 0 later 
           npDataArr = np.zeros(n, dtype=np.float)
        elif cnt >= 1:
           ##Parse data, put rows in list, list appended to a numpy array
           w=xx.split(" ")
           rhead=str(cnt-1)
           clist.append(rhead)
           lookupC[cnt-1]=rhead
           new_list = []
           for item in w:
               new_list.append(float(item))
           npDataArr = np.vstack((npDataArr,new_list))
           dataCnt+=1
        else:
           print("Something is wrong, bail")

        cnt+=1

    ### remove phoney line 0 that established shape.  Find a better way later
    npDataArr=np.delete(npDataArr, 0, 0)
    print("Read ",dataCnt," Datapoints") 
    return lookupC, clist, npDataArr


def main():
    ##Use a class so pointers to objects persist as they are passed by reference
    Params=ParameterClass()  
    Params.M=0
    Params.K=0
    Params.Beta=0
   
    # read file, load data into n x n array npData
    # also return trackCenters, names of each row
    centerLookup,trackCenters,npData= readData() # load Data and Params from file

    finalPath=[] 
    T={}
    tlist=[]
    for j in trackCenters:
        tlist.append(j)
    T['root']=tlist
    n=len(trackCenters)
    print(trackCenters)
    print(centerLookup)
    ##  generate two numbers, that are not equal, between 0 and n
    ##  create a new node name string looking up what is in centerlookup 
             

    bCntr=1
    print("TrackCenters is ",trackCenters)
    while len(trackCenters) > 1:
        print("Nappy roots")
        print(T)
        bCntr+=1
        ####
        #1 #
        ##################################################
        # get the smallest value and its position, row wise
        # 1 Search for smallest value, keep it Row, Col tuple Pos 
        ##################################################
        SmallV, Pos = MinPos(npData) 
        
        ####
        #2 #
        ##################################################
        #  Row is first row and Col is also a row later
        #  that is to be joined with Row. Both Row combine
        ##################################################
        Row=int(Pos[0])
        Col=int(Pos[1])
        print("Lowest point in position ",Row,"x",Col)
        print("Which is ",npData[Row][Col])
        print(npData)
        ## create new point string, Cnew
        c1=centerLookup[Row]
        c2=centerLookup[Col]
        Cnew=c1+'_'+c2
        print("Just created node",Cnew)
        print("Look in ",centerLookup," for it")
       
        cRow=str(Row) 
        cCol=str(Col) 
        for node in centerLookup.values():
            if node==str(Row):
                ARow=centerLookup[Row] 

        for node in centerLookup.values():
            if node==str(Col):
                ACol=centerLookup[Col] 


        print("ok, translated ",Row," x ",Col) 
        print("is now been looked up as",ARow," x ",ACol) 


        # delete old ones from centerLookup dictionary
        print("About to delete Row from centerLookup",ARow)
        print("Heres the before")
        print(centerLookup)
        print("**********")
        del centerLookup[Row] 
        print("Heres the after")
        print(centerLookup)

        print("About to delete Col from centerLookup",ACol)
        print(centerLookup)
        print("**********")
        del centerLookup[Col] 
        print("Heres centerLookup now")
        print(centerLookup)
        
        # add new ones
        centerLookup[Row]=Cnew
        print("centerLookup after adding ",Cnew) 
  
        
        # re order centerLookup to tuck in gaps
        for key, value in centerLookup.items():
            print(key," ",value)
        print("***********")
        print("Re order the data array")
        cntr=0
        tempD={}
        for key, value in centerLookup.items():
            tempD[cntr]=value
            cntr+=1
        centerLookup.clear()
        centerLookup=tempD      

        # re order centerLookup to tuck in gaps
        for key, value in centerLookup.items():
            print(key," ",value)
        print("centerLookup has been reodered")
        
        # remove delets by value
        print("zebra: About to remove", Row, " from trackCenters")
        print("Aka ", c1)
        print("Before: ",trackCenters)
        trackCenters.remove(str(c1)) 
        print("After: ",trackCenters)

        print("zebra: About to remove", Col, " from trackCenters")
        print("Aka ", c2)
        print("Before: ",trackCenters)
        trackCenters.remove(str(c2)) 
        print("After: ",trackCenters)

        trackCenters.append(Cnew)

        print("New trackCenters is",trackCenters)
        print("Now trackCenters is ")
        print(trackCenters)
        ####
        #3 #
        ##################################################
        # Coalse row with d function, here min from each 
        ##############
        
        w=len(npData[0])
        aveArray=AveDist(npData[Row],npData[Col],w)
        print(aveArray)

        NewRow=np.array(aveArray)

        ####
        #4 #
        ##################################################
        #Replace row with newly calced row
        #

        npData=np.insert(npData,Row,[NewRow],axis=0)

        npData=np.delete(npData,Row+1,axis=0)


        ####
        #5 #
        ##################################################

        npData=np.insert(npData,Row,[NewRow],axis=1)

        #print("Col inserted successfully, now delete old one")
        #print(npData)

        npData=np.delete(npData,Row+1,axis=1)
        ####
     
        ####
        #6 #
        ##################################################

        #print("Delete row ",Col)   
        #print(npData[Col])
        npData=np.delete(npData,Col,axis=0)

        npData=np.delete(npData,Col,axis=1)
      

        #print("Row/Col replaced, here is Final at bottom of loop")
        #print(npData)

        print("Center Lookup ",centerLookup)
        print("Track Centers",trackCenters)
        print("Final Path",finalPath)

    print("Done ")
    exit()

         
if __name__ == "__main__":
    main()

