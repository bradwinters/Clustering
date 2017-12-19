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




def Mstep(pCenterz,pData,pHiddenMat):
    Numer=[]
    FinalAns=[]

    npHiddenMat=np.array(pHiddenMat)

    for i in range(len(pCenterz)):  # For each center
       newCenter=[]

       for j in range(len(pData)):  # For each datapoint 
          tNumer=np.multiply(npHiddenMat[i,j],pData[j])
          Numer.append(tNumer)

       # Scalar HiddenMatrix x row j in Data created, sum it
       #print("Done with loop, heres numer added")
       SumNumer=np.sum(Numer,axis=0)
       #print(SumNumer)
       Denomin=onesArrow(npHiddenMat[i])
       #print("Divide ",SumNumer," by",Denomin)
       newCenter=np.divide(SumNumer,Denomin) 
       FinalAns.append(newCenter) 
       Numer=[] # reset for next loop

    return FinalAns 


def eStepNewton(Data,Centerz):
    hMatrix=[]
      
    for i in Centerz:  # Calculate the distance from each point 
       arow=[]
       for j in Data:  # store it
          ## Calculate Numerator
          xy=Edist(i,j)  # distance from current Cnt to Dpt
          xyz=xy**2      # square it here, not in the PF
          if xyz <= 0.0:  # catch 0s
              xyz=0.000000002
          Numerator=1.0/xyz

          # Do the same but for all centers
          CNTRt=0.0
          for Ctr in Centerz:
             yy=Edist(Ctr,j)
             yyy=yy**2
             if yyy <= 0.0:
                 yyy=0.000000002 
             dForce=1.0/yyy
             CNTRt+=dForce

          fa= Numerator/CNTRt
          arow.append(fa)
       hMatrix.append(arow)

    return hMatrix 

class ParameterClass:
    K=0
    M=0
    Beta=0

class CenterClass:
    CenterPos=[]
    Centerz=[]

def Print2D(Centers):
    niceCenter=[]
    for row in Centers:
       for element in row:
           print("%5.3f" % (element),end=" ") 
       print()

def eStepSM(Data,Centerz,BetaF):
    hMatrix=[]
     
    for i in Centerz:  # Calculate the distance from each point 
       arow=[] # re initialize each row of the HM, i.e. a centers pts
       for j in Data:  # store it
          ##  First Calc Numerator 
          xy=Edist(i,j)  # distance from current Cntr to Data Pt
          if xy <= 0.0:  # trap to prevent 0 divides
              xy=0.000000002
          xyz=-1.0*BetaF*xy # add in the Beta Factor, 1 is like Newtonian
    
          Force=math.pow(math.e, xyz) # e to the power -B*Dist, numerator
          #print("Numerator is ",Force)
         
          ##  Calc DeNominator 
          # sum influences of all Centers on our data point 
          CNTRt=0.0
          for Ctr in Centerz:
              yy=Edist(Ctr,j)
              if yy <= 0.0:
                  yy=0.000000002
              yyz=-1.0*BetaF*yy
              dForce=math.pow(math.e, yyz)
              CNTRt+=dForce

          # Finally compute the ratio of Ci to Dj over all Cs to Dj 
          fa=Force/CNTRt
          arow.append(fa)     #  add to this row for all Ds, the j loop 

       hMatrix.append(arow)   # a row is done, start another row or end loop 

    return hMatrix 

def delRow(Array2D,pattrn):
    mp=np.where(np.all(Array2D==pattrn,axis=1))

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


def SumCols(anArray):
    
    #onesArray=np.copy(anArray)
    #onesArray.fill(1)
    onesArray=np.ones(1)
    #print("Sum Array Cols",anArray," times ",onesArray)
    ColSum=np.multiply(anArray,onesArray),
     
    return ColSum 

def onesArrow(anArray):
    
    onesArray=np.copy(anArray)
    onesArray.fill(1)
    #print("Multipy ",anArray," times ",onesArray)
    rowSum=anArray.dot(onesArray),
    #print(" = ",rowSum)
     
    return rowSum 


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
    while bCntr < n-1:
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

        finalPath.append(Cnew)

        # delete old ones from dictionary
        print("About to delete Row ",Row)
        print(centerLookup)
        del centerLookup[Row] 
        print("About to delete Col ",Col)
        print(centerLookup)
        del centerLookup[Col] 
        # add new ones
        centerLookup[Row]=Cnew
  
        # re order centerLookup to tuck in gaps
        for key, value in centerLookup.items():
            print(key," ",value)
        print("***********")
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

        trackCenters.remove(str(Row)) 
        trackCenters.remove(str(Col)) 

        #print("Smallest value is ",SmallV," from rows ",Row,Col)
        #print("Combine these two rows")
        #print(Row,":",npData[Row]) 
        #print(Col,":",npData[Col]) 
        # put these points together to make them into one point

        ####
        #3 #
        ##################################################
        # Coalse row with d function, here min from each 
        ##############
        #  For any method, collect the two rows for analysis
        #  for pt in range(npData[0]:
        #      cntr++
        #      npData[Col][cntr]
        #      npData[Row][cntr]

        
        w=len(npData[0])
        aveArray=AveDist(npData[Row],npData[Col],w)
        print(aveArray)

        NewRow=np.array(aveArray)

        ####
        #4 #
        ##################################################
        #Replace row with newly calced row
        #
        #print("Replace row with newly calced row")
        #print("from old npData")
        #print(npData)
        #print("Replace row ")
        #print(npData[Row])
        #print(" with ")
        #print(NewRow)

        npData=np.insert(npData,Row,[NewRow],axis=0)

        #print(npData)
        #print("Row inserted successfully, now delete old one")

        npData=np.delete(npData,Row+1,axis=0)

        #print("Row deleted successfully")
        #print(npData)

        ####
        #5 #
        ##################################################
        #Replace Col with newly calced row
        #print("Replace Col with newly calced row")
        #print("This should go to position ",Col)

        npData=np.insert(npData,Row,[NewRow],axis=1)

        #print("Col inserted successfully, now delete old one")
        #print(npData)

        npData=np.delete(npData,Row+1,axis=1)

        #print("Col deleted")
        #print(npData)
        ####
     
        ####
        #6 #
        ##################################################

        #print("Delete row ",Col)   
        #print(npData[Col])
        npData=np.delete(npData,Col,axis=0)

        #print("Delte Col ",Row)   
        #print(npData[Row])
        #print("Delte Col ",Col)   
        #print(npData[Col])
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

