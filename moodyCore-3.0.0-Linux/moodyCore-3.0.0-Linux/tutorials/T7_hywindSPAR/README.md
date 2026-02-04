## This is a run script to prepare and run the Nemoh test case (Hywind Spar platform)
# Data was taken from 
# Jonkman, J. 2010, Definition of the Floating System for Phase IV of OC3 
# Technical Report NREL/TP-500-47535, National Renewable Energy Laboratory, 2010
# NB: The mass and COG defined in the input files of this case is the joint COG of platform, nacelle&rotor and tower.
# NB2: The geometry is simplified, where 10m constant diameter truncated tower has been added on top of the 10m high platform, 
# totalling 20m above SWL in "undisplaced" position
# NB3: The mesh resolution is deliberately chosen to favour computational speed in the setup. 
# Be advised that BEM-results should be properly verified in production runs.

## ===== THIS PART IS TO SHOW HOW TO GENERATE NEMOH RESULTS AND IMPORT THEM INTO MOODYCORE SIMULATION ===== ##
moodyPre.exe -nemoh -f oc3_hywind.m
# Execute neccessary nemoh commands 
cd nemoh; 
preProc.exe
solver.exe
postProc.exe
cd ..

# Execute moodyCore
moody.exe -f oc3_hywind.m -o hywind

## ==== THIS PART IS IF YOU DO NOT HAVE NEMOH INSTALLED AND WANT TO USE THE PRECOMPUTED nemohStore RESULTS ===== ##
# Do not run the above. Instead, uncomment below and run: 

# moody.exe -f oc3_hywind.m -o hywind -addInput hydroBody1.bemData nemohStore

## ===== Optional view of results ===== ## 
python ../../API/python/post/moodyPlt.py hywind

# MOODYMARINE NOTE: To view the results in MoodyMarine, please change relative paths to the stl-files to absolute paths in hywind/setup.json 
# alternatively, prior to execution in oc3_hywind.m
