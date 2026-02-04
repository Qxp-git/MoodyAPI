from matplotlib import pyplot as plt
import numpy as np
	
if __name__=="__main__":
	
	# dt 0.005
	t = np.linspace(0,10,10000)
	
	a=0.03;
	w=2*np.pi
	rampT = 2.0
	x = a*np.sin(w*t)
	y= 0*t
	z = -a*np.sin(w*t-0.5*np.pi)
	
	# Ramp values
	tR=t[t<rampT]/rampT
	x[t<rampT] *= tR
	z[t<rampT] *= tR

	# Fairlead initial points
	P1 = [-0.1362, 0.2360, 0.0]
	P2 = [-0.1362, -0.2360, 0.0]
	P3 = [0.2725, 0.0, 0.0]
	
	# Combine values
	X= np.array([t,x+P1[0],y+P1[1],z+P1[2],x+P2[0],y+P2[1],z+P2[2],x+P3[0],y+P3[1],z+P3[2]]).transpose()
	
	plt.axis('equal')
	plt.plot(x,z)
	plt.show()
	
	np.savetxt("fairleadHistory.txt",X)
