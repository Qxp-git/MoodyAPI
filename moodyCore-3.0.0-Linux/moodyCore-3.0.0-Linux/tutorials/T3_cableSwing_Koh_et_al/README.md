Moody tutorial T3
==================
Model scale experiment of a swinging neoprene cable by Koh et al (1999). 
A validation case used to compare moody bending stiffness implementation with 
experimental data in Palm (2020).  

Koh, C., Zhang, Y. and Quek, S. 
Low-tension cable dynamics: Numerical and experimental studies. 
J. Eng. Mech. 1999, 125, 347–354. (1999)

Palm, J. and Eskilsson, C. 
Influence of Bending Stiffness on Snap Loads in
Marine Cables: A Study Using a High-Order
Discontinuous Galerkin Method
J. Marine Science and Engineering, 2020, 8, 795. (2020)


Example below simulates the swinging cable with and without bending stiffness.

Run from command line
---------------------
## The following is a copy of runFromTerminal.sh:

# Run original simulation (with bending stiffness) 
moody.exe -f kohExperiment.m -o kohResult

# Run case without bending stiffness (NB: compressionScale needs to be off to avoid buckling.)
moody.exe -f kohExperiment.m -o EI0 -addInput cableType1.materialModel.EI 0 cableType1.materialModel.compressionScale 0

# Create vtk-output to view the falling cables:
moodyPost.exe kohResult -vtk -dt 0.05 # output every 0.05 s.
moodyPost.exe EI0 -vtk -dt 0.05 # output every 0.05 s.
## <resultName>/VTK/cable.* files can now be opened in paraview, showing position and field tension force. 
# Or--- open result directory from MoodyMarine

# Generate plots for comparing position and tension with and without bending stiffness of the swinging cable
# NOTE: Both simulations above must be run for it to work. 
python post.py 

# Python post-processing dependencies are matplotlib and numpy.


