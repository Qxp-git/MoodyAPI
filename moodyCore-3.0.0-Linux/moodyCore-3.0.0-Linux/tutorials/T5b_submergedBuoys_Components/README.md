# !/bin/bash

# Run simulation of 5 horizontal cables with 2 clumpweights and a cylindrical buoy attached every 50 m. The two clumpweights surround the buoy, which is in the center of the system.  
# The system is pretensioned with 2kN at t=0, and is then released. The simulation shows the decaying motion to the equilibrium.  
moody.x -f moodyInput.m -o moodyResults -endTime 50

# Use default plotCase from moodyPlt to plot time histories of heave for rigidbodies and tension for cables. The case consists of 4 cables, 3 rigid bodies and 0 components. 
# The <save> keyword input also prints the figures into the result folder. 
python ../../API/python/post/moodyPlt.py  moodyResults save

