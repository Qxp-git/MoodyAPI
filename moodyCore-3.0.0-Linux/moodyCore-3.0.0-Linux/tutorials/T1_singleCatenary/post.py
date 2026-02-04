import os
from matplotlib import pyplot as plt
import sys
import numpy as np
sys.path.append("../../API/python/post")
import moodyPlt as mplt
import moodyReader as mr


## Load results. Plot tension.
# case - case name
# lab  - label used in plot 
# period - period time to switch between phase-aligniment to experiments. 
def loadAndPlot(case,lab, period=1.25):
	
	c1=mr.read(case).c[0]
	c1=mr.probeCable(c1,np.array([1]))  
	
	if period == 1.25:
		phaseShift = -0.649;
	else:
		phaseShift =  -2.945;
	
	plt.plot(c1.t+phaseShift,c1.T,linewidth=1.5,label=lab)

if __name__=="__main__":
	case1="lindahl125"	
	case2="lindahl35"
	lab ="numerical"
	
	# Experimental data
	fExp = mr.getAsciiArray("expData.dat",3)
	tExp=fExp[:,0]
	fExp=fExp[:,1:]

	# Plot T=1.25 s case
	f=plt.figure()	
	plt.plot(tExp,fExp[:,0],linewidth=1.5,label="experiment")
	loadAndPlot(case1,lab)	
	ax=plt.gca()
	mplt.frmtTimePlot(ax,[0,15],"Tension (N)")	
	f.savefig("L125.png",bbox_inches="tight",dpi=300)

	# Plot T=3.5 s case
	f=plt.figure()
	plt.plot(tExp,fExp[:,1],linewidth=1.5,label="experiment")
	loadAndPlot(case2,lab,3.5)
	ax=plt.gca()
	mplt.frmtTimePlot(ax,[0,15],"Tension (N)")
	
	f.savefig("L35.png",bbox_inches="tight",dpi=300)

	plt.show()
	 
