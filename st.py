import numpy as np
import math 
import copy 
from random import randint
'''
'''

def AveDist(row1,row2,Width,tCntrs,r,c):

    AvgdRow=[] 
    tAvgdRow=[] 
    wtVector=[]
    Wt1=1.0
    Wt2=1.0
    print("Calculate new row using ")
    print(tCntrs)
    for jj in range(Width):
       facter=tCntrs[jj].count('_') 
       wtVector.append(facter+1)
    print(wtVector)
    print(tCntrs)

    print("Given row and column ",r," and ",c)
    Wt1=wtVector[r]
    Wt2=wtVector[c]

    print("Wts are ")
    print(tCntrs[r],"has Wt1 ",Wt1)
    print(tCntrs[c],"has Wt2:",Wt2)


    for pt in range(Width): 
       if (row1[pt]==0.0 or row2[pt] == 0.0):
          element=0 
       else:
          element=((row1[pt]*Wt1)+(row2[pt]*Wt2))/(Wt1+Wt2)
          print(row1[pt],"*",Wt1," plus ",row2[pt],"*",Wt2," / ",Wt1,"+",Wt2,"=",element)
           
          telement=((row1[pt])+(row2[pt]))/(Wt1*Wt2)
          print(row1[pt]," plus ",row2[pt]," / ",Wt1,"*",Wt2,"=",telement)
       AvgdRow.append(element)
    print("just computed ",AvgdRow)
    return AvgdRow

def WAve(Row,Col,Data):
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$") 
    print("Row is ", Row)
    print("Col is ", Col)
    print("Data is ")
    print(Data)

def gapCompress(aDict):
    cntr=0
    nogapsDict={}
    thegap=-1
    entryCnt=len(aDict)+1
    maxV=-1
    
    # find the largest key 
    for key, value in aDict.items():
        if key > maxV:
            maxV=key
    # if the max key matches the size, its compressed already
    if maxV==len(aDict)-1:
         return aDict 

    print("Size and max key not are equal, contin")
    for i in range(entryCnt):
        try:
           print("load ",aDict[i]," into tofix ",i)
        except:
           print("failed")
           print("Gap at ",i)
           thegap=i

    if thegap > 0:
         for kk in range(thegap):
             nogapsDict[kk] = aDict[kk] 
         for jj in range(thegap,len(aDict)):
             nogapsDict[jj] = aDict[jj+1] 

         ## for key, value in centerLookup.items():
         print(nogapsDict)
         return nogapsDict 
    else:
         return aDict

def ParseU(astring):
    facter=astring.count('_') 
    return facter



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
    #f = open('data1.dat', 'r')   #Smaller dataset 
    f = open('data2.dat', 'r')   #Smaller dataset 
    #f = open('youtube.dat', 'r')   #Smaller dataset 
    #f = open('test.dat', 'r')   # use on test after renaming weird names 
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
    #Use a class so pointers to objects persist as they are passed by reference
    Params=ParameterClass()  
    Params.M=0
    Params.K=0
    Params.Beta=0
   
    # read file, load data into n x n array npData
    # also return trackCenters, names of each row

    centerLookup,trackCenters,npData= readData() #load Data and Params from file

    finalPath=[] 
    answer=[] 
    T={}
    tlist=[]
    trackFactr={}
    for j in trackCenters:
        tlist.append(j)
        trackFactr[j]=1

    T['root']=tlist
    n=len(trackCenters)
    ##  generate two numbers, that are not equal, between 0 and n
    ##  create a new node name string looking up what is in centerlookup 
             

    while len(trackCenters) > 1:
        print("*** Top of the loop   *****")
        print(npData)
        print("TrackCenters is ")
        print(trackCenters)
        print("centerLookup is ")
        print(centerLookup)
        ####
        #1 #
        ##################################################
        # get the smallest value and its position, row wise
        # 1 Search for smallest value, keep it Row, Col tuple Pos 
        ##################################################
        SmallV, Pos = MinPos(npData) 
        Row=int(Pos[0])
        Col=int(Pos[1])
        print("&&&  Smallest value is now ",SmallV) 
        ####
        #3 #
        ##################################################
        # Coalse row with d function, here min from each 
        ##############
        
        w=len(npData[0])
        aveArray=AveDist(npData[Row],npData[Col],w,centerLookup,Row,Col)
        
        NewRow=np.array(aveArray)

        ####
        #2 #
        ##################################################
        #  Row is first row and Col is also a row later
        #  that is to be joined with Row. Both Row combine
        ##################################################

        ## create new point string, Cnew
        c1=centerLookup[Row]
        c2=centerLookup[Col]
        Coalest1=0
        Coalest2=0
        Coalest1=c1.count('_')
        Coalest2=c2.count('_')
        print("C1 is ",c1)
        print("Cf1 is ",Coalest1)
        print("C2 is ",c2)
        print("Cf2 is ",Coalest2)

        if Coalest1==0 and Coalest2==0: 
            Cnew=c1+'_'+c2
        elif Coalest2 >= Coalest1:
            Cnew=c1+'_'+c2
        else:
            Cnew=c2+'_'+c1

        answer.append(Cnew) 
        cRow=str(Row) 
        cCol=str(Col) 

        for node in centerLookup.values():
            if node==str(Row):
                ARow=centerLookup[Row] 

        for node in centerLookup.values():
            if node==str(Col):
                ACol=centerLookup[Col] 



        # delete old ones from centerLookup dictionary
        del centerLookup[Row] 

        del centerLookup[Col] 
        
        # add new ones
        centerLookup[Row]=Cnew
        
        # re order centerLookup to tuck in gaps
        #for key, value in centerLookup.items():
        #    print(key," ",value)
        centerLookup=gapCompress(centerLookup)

        cntr=0
        tempD={}
        for key, value in centerLookup.items():
            tempD[cntr]=value
            cntr+=1
        centerLookup.clear()
        centerLookup=tempD      

        
        # remove deletes by value
        trackCenters.remove(str(c1)) 
        trackCenters.remove(str(c2)) 

        trackCenters.append(Cnew)

       

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


        npData=np.delete(npData,Row+1,axis=1)
        ####
     
        ####
        #6 #
        ##################################################

        npData=np.delete(npData,Col,axis=0)

        npData=np.delete(npData,Col,axis=1)
      

    print("Done ")
    for line in answer:
        out=line.split('_')
        outline=""
        for o in out:
            oo=int(o)+1
            outline+=str(oo)+" "
            
        print(outline[:-1])

    f = open("answer.dat","w")
    for pair in answer:
        aline=""
        p=pair.split('_')
        for j in p:
            ii=int(j)+1
            aline+=(str(ii)+" ")
        f.write(str(aline))
        f.write("\n")
    f.close()

    #for pair in answer:
    #    p=pair.split('_')
    #    for j in p:
    #        k=int(j)+1 
    #        print(k,end=" ")
    #    print()

         
if __name__ == "__main__":
    main()

