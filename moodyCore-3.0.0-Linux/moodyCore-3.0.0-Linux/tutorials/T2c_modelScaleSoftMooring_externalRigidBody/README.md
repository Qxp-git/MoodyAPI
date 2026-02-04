Moody tutorial T2c
=================
Model scale soft mooring run via API. Three catenary chains attached to a cylindrical buoy. 
Time history of the 6 dof rigid body motion (time,x,y,z,roll,pitch,yaw) in [m] and [rad] respectively are 
pre-generated and used via the API as externalRigidBody motion. Fairleads are connected to this reference frame as slaves.  
An additional figure compared to T2a and T2b is plotted in post.py. It shows the resulting mooring forces and moments in the 6 dofs of the body.  

Run from command line
---------------------
source ../../etc/bashrcMoody 
python makeHistory.py
testAPI.x mooringSystem.m fairleadHistory.txt
python post.py

Python post-processing dependencies are matplotlib and numpy.


