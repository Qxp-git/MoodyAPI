# !/bin/bash
# A complete run-script to create a hydrobody simulation. 
# This script assumes that both moodyCore and the boundary element solver Nemoh are installed on the system PATH.
# Note: To run moody.exe directly with existing nemoh results. Change to: hydroBody1.bemData = nemohStore in ellipsoid.m and run stage 4 and 5 directly. 

# 0 : moodyPre -nemoh --> create a nemoh project from moody input file settings.
moodyPre.exe -nemoh -f ellipsoid.m 

# 1 : preProc.exe --> nemoh stage 1,
cd nemoh; 
preProc.exe

# 2 : solver.exe --> nemoh stage 2, 
solver.exe # this takes a few minutes 

# 3 : postProc.exe --> nemoh stage 3
postProc.exe
cd ..; # back up to original location.

# 4 : moody.exe --> run dynamics. Default output is folder: ellipsoid 
moody.exe -f ellipsoid.m 

# 5 : view results (in python or through moodymarine GUI)
python ../../API/python/post/moodyPlt.py ellipsoid

# NB1 To view result in moodymarine, open ellipsoid/setup.json and change hydroBody1.meshName to an absolute path (to see the body). 
# NB2 To run the same simulation steps in moodymarine: 
#     Open ellipsoid.m and use browse to select meshName for both hydroBody and hydroBody.bemInput


