import sys
import os
from matplotlib import pyplot as plt
sys.path.append("../../API/python/post")
import moodyPlt	as mplt
import moodyReader as mr
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
cMap = plt.get_cmap("tab10")

# Plot cable position at time t, lab is label
def plotPosition(ax,c,t,lab,**kwargs):

	ct=mr.sampleCable(c,np.array([t]))	
	p=np.squeeze(ct.p)
	if "3d" in kwargs:
		ax.plot(p[:,0],p[:,1],p[:,2],linewidth=1.5,label=lab,**kwargs)
	else:
		ax.plot(p[:,0],p[:,2],linewidth=1.5,label=lab,**kwargs)

# Load cable and plot tension force at fairlead
def loadAndPlot(case,**kwargs):
	c=mr.read(case).c[0]
	
	
	c1=mr.probeCable(c,np.array([0]))  	
	
	plt.plot(c1.t,c1.T,**kwargs)
	
	return c
	
if __name__=="__main__":

	if len(sys.argv) > 1:
		case=sys.argv[1]
	else:
		case="moodyResults"

	# Plot tension
	f=plt.figure()		
	c1=loadAndPlot("kohResult",linewidth=1.5,label="Bending stiffness")
	c2=loadAndPlot("EI0",linewidth=1.5,label="Flexible")

	# c2=loadAndPlot(case+"/cable2",linestyle='--',linewidth=1.5,label="$c_2$")
	# c3=loadAndPlot(case+"/cable3",linewidth=1.5,label="$c_3$")		
	
	# Frmt plot
	ax=plt.gca()
	mplt.frmtTimePlot(ax,[0,5],"Fairlead tension (N)")	
	f.savefig("tension.png",bbox_inches="tight",dpi=300)

		
	## Also, plot the position of the cables:	
	fig = plt.figure()
	ax = plt.gca()
	# ax = fig.add_subplot(111, projection='3d')
	
	# c1	
	plotPosition(ax,c1,0.0,"Bending stiffness")	
	plotPosition(ax,c2,0.0,"Flexible")	
	# c2
	# plotPosition(ax,c2,0.0,"$c_2$")	
	# c3
	# plotPosition(ax,c3,0.0,"$c_3$")	
	
	# Format plot:
	ax.set_xlabel('x (m)')
	ax.set_ylabel('z (m)')
	#	ax.set_zlabel('z (m)')
	# ax.xaxis.labelpad=20
	# ax.yaxis.labelpad=20
	# ax.zaxis.labelpad=20	
	# ax.set_zticks(np.linspace(-0.9,-0.1,5))
	mplt.frmtPlot(ax)	
	
	# Save start point
	fig.savefig("initialPosition.png",bbox_inches="tight",dpi=300)
	
	# Loop and plot position envelope
	for t in np.arange(0,1.5,0.1):
		
		plotPosition(ax,c1,t,"EI",color=cMap(0))		
		plotPosition(ax,c2,t,"$EI=0$",color=cMap(1))		
		# plotPosition(ax,c3,t,"$c_3$",color=cMap(2))	
		
	fig.savefig("positionEnvelope.png",bbox_inches="tight",dpi=300)
	plt.show()
	
