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


def readData(px):
    '''
    Open hardcoded file, parse data anticipataed but may change
    Load just data into a numpy array, 
    '''
    #f = open('wk2_1.dat', 'r')   #Smaller dataset 
    f = open('wk2_2.dat', 'r')  #Larger test dataset 
    #f = open('book.dat', 'r')   #Smaller dataset 
    cnt=0
    dataCnt=0
    Dataflag=False
    print("Loading data . . .")
    # K is used to grab the first K lines as clusters, don't consider them
    # Data at this time, that may not be correct
    for line in f:
        xx=line.rstrip() # get rid of cr
        if cnt==0:       # known line to contain only K and M
           v=xx.split(' ')
           px.K=int(v[0])
           px.M=int(v[1])
           ##Use K,M to Dim numpy arrays to build, delete these rows later 
           DataArr = np.zeros((px.M), dtype=np.float)
        elif cnt==1:
           px.Beta=float(xx)
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
           DataArr = np.vstack((DataArr,new_list))
           dataCnt+=1
        else:
           print("Something is wrong, bail")

        cnt+=1
    print("Read ",dataCnt," Datapoints") 
    return DataArr


def main():
    ##Use a class so pointers to objects persist as they are passed by reference
    Params=ParameterClass()  
    Params.M=0
    Params.K=0
    Params.Beta=0
    
    Data= readData(Params) # load Data and Params from file
    ### remove phoney line 0 that established shape.  Find a better way later
    Data=np.delete(Data, 0, 0)
    #print("Data is ",Data)

    Centers = np.zeros((Params.M), dtype=np.float)
    print("Copy first K data points into Centers")
    Centers=copy.deepcopy(Data[:Params.K])

    #print("Cleaned Centers is ")
    #print(Centers)

    
    LoopCnt=1

    print("K is ",Params.K," M is ",Params.M," Beta is ", Params.Beta)
    #Params.Beta=1  # Test closest to Newtonian method via stat mechanics method 

    while LoopCnt <= 100:
        ############################################################
        #  Map centers to data pts, keep the distance as well
        #  Returns Array of 3 part tuple, (Center Array, DataPt Array and Dist)
        #  Centers to Clusters Phase
        # 
        #Build HiddenMatrix as Sphere of influence: All Centers=>All DataPts
        # (1)  E Step
        # Two ways
        # Pick eStep from Statistical Mechanics or Newtonian methods
        #

        HiddenMatrix=eStepSM(Data,Centers,Params.Beta)
        
        #HiddenMatrix=eStepNewton(Data,Centers)

        #for m in HiddenMatrix:
        #   for n in m:
        #      print("%5.3f" % (n),end=" ") 
        #   print()


        # (1)  M Step
        #print("Starting M step, Centers, Data and HD dimensions are")

        theanswer=Mstep(Centers,Data,HiddenMatrix)

        Centers=np.array(theanswer)
        #print(Centers)
       
        LoopCnt+=1
        print("Loop Count ",LoopCnt)
        #  End Loop 

    print("*******Final Centers is ****")

    Print2D(Centers)
         
if __name__ == "__main__":
    main()
