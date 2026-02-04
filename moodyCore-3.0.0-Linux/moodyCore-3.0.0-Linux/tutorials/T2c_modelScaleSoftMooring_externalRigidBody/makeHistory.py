from matplotlib import pyplot as plt
import numpy as np
	
if __name__=="__main__":
	
	# dt 0.005
	t = np.linspace(0,10,10000)
	
	a=0.03;		   					# heave amplitude
	pitchAmp = 0*np.pi/180; 		# pitch amplitude (rad)
	pitchPhase = 60*np.pi/180; 		# pitch phase (rad)
	rampT = 2.0 					# ramp time
	w=2*np.pi						# angular frequency for 2Hz motion
	
	x = a*np.sin(w*t)
	y= 0*t
	z = -a*np.sin(w*t-0.5*np.pi)
	phi = pitchAmp*np.sin(w*t-0.5*np.pi+pitchPhase);	
	# Ramp values
	tR=t[t<rampT]/rampT
	x[t<rampT] *= tR
	z[t<rampT] *= tR
	phi[t<rampT] *= tR

	# Combine values
	X= np.array([t,x,y,z,0*t,phi,0*t]).transpose()
	
	plt.axis('equal')
	plt.plot(x,z)
	plt.show()
	
	np.savetxt("fairleadHistory.txt",X)
