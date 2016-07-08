# radarProcess.py
#
# process the SANAE and HALLEY superdarn data
# sort by month, beam to get the ground scatter
# files are fitacf processed from rawacf
# lots of data, save by month and beam and gate
# 16 beams and 75 gates 
#
# LKS, SANSA, April 2016
#
import numpy as np
import glob
import os
import pickle
import datetime
import matplotlib.pyplot as plt
#
# starting parameters
curYear=2011
endYear=2016 # make it one more than your last year
curMonth=1
curDT=datetime.datetime(curYear,curMonth,1,0,0,0)
#
# first load in davitpy on my machine
os.chdir('/Users/loisks/davitpy/davitpy')
from davitpy import * 
#
# great now go to where the data is
path='/Users/loisks/Documents/ResearchProjects/RadarProject/'
dataPath='/Volumes/KEPLER/RadarProject/SANAE_fitacf/'
os.chdir(dataPath+str(curDT.year)+'_fitacf')
files=glob.glob('*.fitacf')
#
# file format:
# 'YYYYMMDD.HRMM.SS'
#
#
# empty dictionaries and arrays
yesbeamDicts=[ [ 0 for jj in range(75)] for ii in range(16)]
nobeamDicts=[ [ 0 for jj in range(75)] for ii in range(16)]
#timeDicts=[ [ [] for jj in range(75)] for ii in range(16)]
# now we need to loop the files in the list
while curDT.year < endYear:
   
  for iFile in range(len(files)):
    #
    # extract the datetime from the filename
    fileName=files[iFile]
    year=int(fileName[0:4])
    month=int(fileName[4:6])
    day=int(fileName[6:8])
    hour=int(fileName[9:11])
    minute=int(fileName[11:13])
    second=int(fileName[14:16])
    dt=datetime.datetime(year,month,day,hour,minute,second)
    dtend=dt+datetime.timedelta(days=1)

    if ((dt.year > curDT.year) or (dt.month > curDT.month)):
        # save the file and start afresh
        os.chdir(path+'SANAE_PROCESSED')
        #
        # create year directory
        dirYear=str(curDT.year)
        if not os.path.exists(dirYear):
            os.umask(0) # unmask if necessary
            os.makedirs(dirYear) 
        os.chdir(dirYear)#
        # create month directory
        dirMonth=str(curDT.month)
        if not os.path.exists(dirMonth):
            os.umask(0) # unmask if necessary
            os.makedirs(dirMonth)
        os.chdir(dirMonth)
        for iBeam in range(16):
         # create beam directory
         dirBeam='Beam='+str(iBeam)
         if not os.path.exists(dirBeam):
            os.umask(0) # unmask if necessary
            os.makedirs(dirBeam)
         os.chdir(dirBeam)
         for iGate in range(75):
           dirGate='Gate='+str(iGate)
           if not os.path.exists(dirGate):
             os.umask(0) # unmask if necessary
             os.makedirs(dirGate)
           os.chdir(dirGate)

           #
           # finally save the files
           # just use pickle
           pickle.dump(yesbeamDicts[iBeam][iGate], open(dirYear+'_'+dirMonth+'_'+dirBeam+'_'+dirGate+'_backscatter.p', 'wb'))
           pickle.dump(nobeamDicts[iBeam][iGate], open(dirYear+'_'+dirMonth+'_'+dirBeam+'_'+dirGate+'_nobackscatter.p', 'wb'))
          # pickle.dump(timeDicts[iBeam][iGate], open(dirYear+'_'+dirMonth+'_'+dirBeam+'_'+dirGate+'_time.p', 'wb'))
           os.chdir('..')
         os.chdir('..')           
        # now return to data files
        if curMonth < 11:
            curDT=datetime.datetime(curDT.year, curDT.month + 1,1)
             
        os.chdir(dataPath+str(curDT.year)+'_fitacf')
        # empty lists 
        yesbeamDicts=[ [ 0 for jj in range(75)] for ii in range(16)]
        nobeamDicts=[ [ 0 for jj in range(75)] for ii in range(16)]
        #timeDicts=[ [ [] for jj in range(75)] for ii in range(16)]         

        
    # continue to process
    # get the radar data via davity py
    myPtr= pydarn.sdio.radDataRead.radDataOpen(dt, 'san', eTime=dtend,fileType='fitacf',fileName=fileName, src='local')
    myBeam= pydarn.sdio.radDataRead.radDataReadAll(myPtr)
    # loop on the beam
    for iBeam in range(len(myBeam)):
       bmnum=myBeam[iBeam].bmnum
       time=myBeam[iBeam].time
       gflg=myBeam[iBeam].fit.gflg
       slist=myBeam[iBeam].fit.slist
       #
       # sort the data appropriately
       # by beam
       # by range gate
       # only include times of backscatter
       try:
          slist=np.array(slist)
          gflg=np.array(gflg)
          yeslist=slist[gflg==1]
          nolist=slist[gflg==0]
          yesgflg=gflg[gflg==1]
          nogflg=gflg[gflg==0]
          
          for iR in range(len(yeslist)):
              yesbeamDicts[bmnum][yeslist[iR]]+=1# gives a total number of points
              #timeDicts[bmnum][yeslist[iR]]+=[time]
          for iNo in range(len(nolist)):
              nobeamDicts[bmnum][nolist[iNo]]+=1 # gives a total number of points
       except(IndexError):
           print('No Ground Scatter Data')
  # if end of files has been reached, add a year and continue
  os.chdir(path+'SANAE_PROCESSED')
   #
   # create year directory
  dirYear=str(curDT.year)
  if not os.path.exists(dirYear):
      os.umask(0) # unmask if necessary
      os.makedirs(dirYear) 
  os.chdir(dirYear)#
  # create month directory
  dirMonth=str(curDT.month)
  if not os.path.exists(dirMonth):
      os.umask(0) # unmask if necessary
      os.makedirs(dirMonth)
  os.chdir(dirMonth)
  for iBeam in range(16):
         # create beam directory
         dirBeam='Beam='+str(iBeam)
         if not os.path.exists(dirBeam):
            os.umask(0) # unmask if necessary
            os.makedirs(dirBeam)
         os.chdir(dirBeam)
         for iGate in range(75):
           dirGate='Gate='+str(iGate)
           if not os.path.exists(dirGate):
             os.umask(0) # unmask if necessary
             os.makedirs(dirGate)
           os.chdir(dirGate)
           #
           # finally save the files
           # just use pickle
           pickle.dump(yesbeamDicts[iBeam][iGate], open(dirYear+'_'+dirMonth+'_'+dirBeam+'_'+dirGate+'_backscatter.p', 'wb'))
           pickle.dump(nobeamDicts[iBeam][iGate], open(dirYear+'_'+dirMonth+'_'+dirBeam+'_'+dirGate+'_nobackscatter.p', 'wb'))
           #pickle.dump(timeDicts[iBeam][iGate], open(dirYear+'_'+dirMonth+'_'+dirBeam+'_'+dirGate+'_time.p', 'wb'))
           os.chdir('..')
         os.chdir('..')           
  # update the dates 
  curDT=datetime.datetime(curDT.year + 1, 1, 1, 0, 0)
  os.chdir(dataPath+str(curDT.year)+'_fitacf')
  files=glob.glob('*.fitacf')
  # just set up blank ones 
  yesbeamDicts=[ [ 0 for jj in range(75)] for ii in range(16)]
  nobeamDicts=[ [ 0 for jj in range(75)] for ii in range(16)]
  #timeDicts=[ [ [] for jj in range(75)] for ii in range(16)]
