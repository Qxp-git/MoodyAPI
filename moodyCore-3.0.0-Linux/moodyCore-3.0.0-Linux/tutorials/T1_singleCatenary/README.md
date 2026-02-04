Moody tutorial T1
=================
Validation of single catenary chain in still water. 
---
Experimental data from:
L. Bergdahl,  J. Palm, C. Eskilsson and J. Lindahl. Dynamic Model Experiment of a Mooring Cable. J. Mar. Sci. Eng. 3, (2015)
Original experiment by Jan Lindahl, Chalmers University of Technology 1984. 
---

Run from command line
---------------------
source ../../etc/bashrcMoody 
moody.x -f lindahl125.m
moody.x -f lindahl35.m
python post.py

Python post-processing dependencies are matplotlib and numpy.

Alternative modification style for lindahl35 case
-------------------------------------------------
moody.x -f lindahl125.m -o lindahl35 -endTime 20 -addInput bc2.period 3.5 bc2.rampTime 3.5



Run from Matlab
---------------
Start matlab and execute runFromMatlab.m
Edit the script and uncomment moodyMovie option to create video of mooring chain motion.


