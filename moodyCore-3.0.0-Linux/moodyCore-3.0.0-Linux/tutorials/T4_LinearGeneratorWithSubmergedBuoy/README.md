# !/bin/bash

# Run simulation of a submerged version of the Uppsala University wave energy converter. A linear generator with end-stop springs and PTO is mounted on the bottom, connected via a component spring to a submerged rigid cylinder buoy.
# Wave excitation is due to Froude-Krylov forces, inertial forces and drag forces acting on the cylinder from the Morison approximation.
moody.exe -f UUwecMoody.m

# Use default plotCase from moodyPlt to plot time histories of heave for rigidbodies and tension for cables or components. The case consists of 1 component and two rigid bodies.
# The <save> keyword input also prints the figures into the result folder. 
python $moodyPyDir/moodyPlt.py  UUwecMoody save

