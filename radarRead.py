# radarRead.py
#
# read in the radar process pickle files
# combine together
# do some statistics
#
# LKS, SANSA, April 2016
#
# imports 
import numpy as np
import glob
import os
import pickle
import datetime
import matplotlib.pyplot as plt
#
# we need to open all the files
# and combine the totals together
# also check for seasonal effects
# look at davitpy FOV stuff for making a map 
#
# starting parameters
curYear=2010
endYear=2016 # make it one more than your last year
curMonth=1
curDT=datetime.datetime(curYear,curMonth,1,0,0,0)
dataPath='/Users/loisks/Documents/ResearchProjects/RadarProject/SANAE_Processed/'
dataSave='/Users/loisks/Documents/ResearchProjects/RadarProject/Plots'
#
# first load in davitpy on my machine
os.chdir('/Users/loisks/davitpy/davitpy')
from davitpy import * 
#
# great now go to where the data is
yesbeamDictAll=[ [ 0 for jj in range(75)] for ii in range(16)]
nobeamDictAll=[ [ 0 for jj in range(75)] for ii in range(16)]
yesbeamDictWinter=[ [ 0 for jj in range(75)] for ii in range(16)]
nobeamDictWinter=[ [ 0 for jj in range(75)] for ii in range(16)]
yesbeamDictSpring=[ [ 0 for jj in range(75)] for ii in range(16)]
nobeamDictSpring=[ [ 0 for jj in range(75)] for ii in range(16)]
yesbeamDictSummer=[ [ 0 for jj in range(75)] for ii in range(16)]
nobeamDictSummer=[ [ 0 for jj in range(75)] for ii in range(16)]
yesbeamDictFall=[ [ 0 for jj in range(75)] for ii in range(16)]
nobeamDictFall=[ [ 0 for jj in range(75)] for ii in range(16)]

try:
 while curDT.year != endYear:
    os.chdir(dataPath+str(curDT.year) + '/' + str(curDT.month))
    for iBeam in range(16):
        os.chdir('Beam='+str(iBeam))
        for iGate in range(75):
            os.chdir('Gate='+str(iGate))
            fileNameno=str(curDT.year)+'_'+str(curDT.month)+'_Beam='+str(iBeam)+'_Gate='+str(iGate)+'_nobackscatter.p'
            fileNameyes=str(curDT.year)+'_'+str(curDT.month)+'_Beam='+str(iBeam)+'_Gate='+str(iGate)+'_backscatter.p'

            loadedYes=pickle.load(open(fileNameyes, 'rb'))
            loadedNo=pickle.load(open(fileNameno, 'rb'))
            yesbeamDictAll[iBeam][iGate]+=loadedYes
            nobeamDictAll[iBeam][iGate]+=loadedNo
            #
            # sort by season
            if ((curDT.month == 4) or (curDT.month == 5) or (curDT.month == 6)):
                yesbeamDictFall[iBeam][iGate]+=loadedYes
                nobeamDictFall[iBeam][iGate]+=loadedNo
            elif ((curDT.month == 7) or (curDT.month == 8) or (curDT.month == 9)):
                yesbeamDictWinter[iBeam][iGate]+=loadedYes
                nobeamDictWinter[iBeam][iGate]+=loadedNo
            elif ((curDT.month == 10) or (curDT.month == 11) or (curDT.month == 12)):
                yesbeamDictSpring[iBeam][iGate]+=loadedYes
                nobeamDictSpring[iBeam][iGate]+=loadedNo
            else:
                yesbeamDictSummer[iBeam][iGate]+=loadedYes
                nobeamDictSummer[iBeam][iGate]+=loadedNo               
            
            os.chdir('..')
        os.chdir('..')
    if curDT.month < 12:
        curDT=datetime.datetime(curDT.year, curDT.month+1,1,0)
    else:
        curDT=datetime.datetime(curDT.year+1, 1, 1, 0)
#
# complete data set should be loaded now
# let's get some percentages first?

except: 
   percentYesAll=[ [ 0 for jj in range(79)] for ii in range(16)]
   percentYesSummer=[ [ 0 for jj in range(79)] for ii in range(16)]
   percentYesWinter=[ [ 0 for jj in range(79)] for ii in range(16)]
   percentYesSpring=[ [ 0 for jj in range(79)] for ii in range(16)]
   percentYesFall=[ [ 0 for jj in range(79)] for ii in range(16)]
   for iBeam in range(16):
       for iGate in range(4,79):
           percentYesAll[iBeam][iGate]=100.0*(yesbeamDictAll[iBeam][iGate-4]/(1.0*(nobeamDictAll[iBeam][iGate-4]+yesbeamDictAll[iBeam][iGate-4])))
           percentYesSummer[iBeam][iGate]=100.0*(yesbeamDictSummer[iBeam][iGate-4]/(1.0*(nobeamDictSummer[iBeam][iGate-4]+yesbeamDictSummer[iBeam][iGate-4])))
           percentYesFall[iBeam][iGate]=100.0*(yesbeamDictFall[iBeam][iGate-4]/(1.0*(nobeamDictFall[iBeam][iGate-4]+yesbeamDictFall[iBeam][iGate-4])))
           percentYesSpring[iBeam][iGate]=100.0*(yesbeamDictSpring[iBeam][iGate-4]/(1.0*(nobeamDictSpring[iBeam][iGate-4]+yesbeamDictSpring[iBeam][iGate-4])))
           percentYesWinter[iBeam][iGate]=100.0*(yesbeamDictWinter[iBeam][iGate-4]/(1.0*(nobeamDictWinter[iBeam][iGate-4]+yesbeamDictWinter[iBeam][iGate-4])))
   #
   # try to make the FOV plot
   #
   from matplotlib.transforms import Affine2D
   import mpl_toolkits.axisartist.floating_axes as floating_axes
   import numpy as np
   import mpl_toolkits.axisartist.angle_helper as angle_helper
   from matplotlib.projections import PolarAxes
   from mpl_toolkits.axisartist.grid_finder import (FixedLocator, MaxNLocator,
                                                 DictFormatter)
   def setup_axes3(fig, rect,ra0,ra1):
    """
    Sometimes, things like axis_direction need to be adjusted.
    """

    # rotate a bit for better orientation
    tr_rotate = Affine2D().translate(0, 0)
    gl1=5

    # scale degree to radians
    tr_scale = Affine2D().scale(3.5*np.pi/180., 1.)

    tr = tr_rotate + tr_scale + PolarAxes.PolarTransform()

   
    tick_formatter1 = angle_helper.FormatterHMS()
    r_labels=['0', '4', '8', '12', '16']
    r_locs = np.linspace(ra0,ra1,gl1)
    r_ticks =  zip(r_locs, r_labels)
    
    #grid_locator1 = angle_helper.LocatorHMS(FixedLocator([v for v, s in r_ticks]))
    r_ticks=DictFormatter(dict(r_ticks))
    grid_locator2 = MaxNLocator(5)
    cz0, cz1 = 0, 79
    grid_helper = floating_axes.GridHelperCurveLinear(
        tr, extremes=(ra0, ra1, cz0, cz1),
        grid_locator1=grid_locator2,
        grid_locator2=grid_locator2,
        #tick_formatter1=r_ticks,
        tick_formatter2=None)

    
    ax1 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
    fig.add_subplot(ax1)
    plt.subplots_adjust(right=0.6, top=0.8, bottom=0.15)

    # adjust axis
    ax1.axis["left"].set_axis_direction("bottom")
    ax1.axis["right"].set_axis_direction("top")

    ax1.axis["bottom"].set_visible(False)
    ax1.axis["top"].set_axis_direction("bottom")
    ax1.axis["top"].toggle(ticklabels=True, label=True)
    ax1.axis["top"].major_ticklabels.set_axis_direction("top")
    ax1.axis["top"].label.set_axis_direction("top")

    ax1.axis["left"].label.set_text(r"Range Gates")
    ax1.axis["top"].label.set_text(r"Beam")
   # ax1.set_xticklabels( r_labels )
    # create a parasite axes whose transData in RA, cz
    aux_ax = ax1.get_aux_axes(tr)

    aux_ax.patch = ax1.patch  # for aux_ax to have a clip path as in ax
    ax1.patch.zorder = 0.9  # but this has a side effect that the patch is
    # drawn twice, and possibly over some other
    # artists. So, we decrease the zorder a bit to
    # prevent this.

    return ax1, aux_ax


##########################################################
#
# we have percent yes in beam x gate
# need to add 4 more gates
seasons=[percentYesAll, percentYesWinter, percentYesSummer, percentYesFall, percentYesSpring]
labels=['All', 'Winter', 'Summer', 'Fall', 'Spring']
for iPlot in range(len(labels)):
    fig = plt.figure(1, figsize=(13, 9))
    theta =np.array(range(16))#*5.6*np.pi/180.0  # in degrees
    radius = np.array(range(79))
    ax3, aux_ax3 = setup_axes3(fig, 111, np.min(theta),np.max(theta))
    vmin=0
    vmax=100
    X,Y=np.meshgrid(theta,radius)
    col=aux_ax3.pcolormesh(X,Y, np.array(seasons[iPlot]).transpose(), cmap='jet', vmin=vmin, vmax=vmax)
    #cbaxes = fig.add_axes([0.75, 0.15, 0.03, 0.75])
    #cb = plt.colorbar(col, cax = cbaxes,ticks=range(vmin, vmax+1, 20))
    #cb.set_label('Percentage of Backscatter Times', fontsize=30)
    aux_ax3.grid(True, lw=4)
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}
    plt.rc('font', **font)
    
    os.chdir(dataSave)
    plt.savefig(labels[iPlot]+'_fan_percentage.pdf', transparent=True)



from mpl_toolkits.basemap import Basemap
plt.figure()
m = Basemap(projection='spstere',boundinglat=-65,lon_0=90,resolution='l')
m.drawcoastlines()
m.drawparallels(np.arange(-80.,81.,10.), labels=[1,1,0,0])
m.drawmeridians(np.arange(-180.,181.,20.), labels=[1,1,0,0])
x,y=m(357.15,-71.68)
m.scatter(x,y,30,marker='o',color='k')
plt.savefig('mapofAnc.pdf', transparent=True)
# now add the radar data
os.chdir('..')









