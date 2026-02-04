Moody tutorial T2b
=================
Model scale soft mooring run via API. Three catenary chains attached to a cylindrical buoy. 
Time histories of each fairlead are pre-generated and used via the API as externalPoint motions.  


Run from command line
---------------------
source ../../etc/bashrcMoody 
python makeHistory.py
testAPI.x mooringSystem.m fairleadHistory.txt
python post.py

Python post-processing dependencies are matplotlib and numpy.


