import sys
from matplotlib import pyplot as plt
sys.path.append("../../API/python/post")
import moodyPlt	as mplt
import moodyReader as mr

# Read case
d=mr.read('UUwecMoody');
# Default plot case 
mplt.plotCase(d);

## Extract body data
buoy= d.b[0]    # get buoy
gen = d.b[1];   # get generator

## Vertical forces on buoy (column indices in _forces.dat) 
inds = [8,14,20] # 2 for FnetBuoyancy -- skipped
labs = ['FaddFK','Fdrag','Fext']; # " Fnb" -- skipped
[plt.plot(buoy.t,buoy.forces[inds[ii],:],label=labs[ii]) for ii in range(len(inds)) ]
plt.xlabel("Time (s)")
plt.ylabel("Vertical forces on buoy (N)")
plt.legend()

plt.show()
