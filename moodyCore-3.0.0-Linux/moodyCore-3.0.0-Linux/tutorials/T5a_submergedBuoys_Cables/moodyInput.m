% Simulation settings ---% 
simulation ={
	time= {
		start = 0
		end = 10
		% dt = 1e-2
		cfl = 0.9
	}
	statics.solve = 0;
	statics.relax = 0;
	% statics.relaxExponent = 1.0;
	% statics.timestep = 0.01;
	
	
}

%--- Points ---% 
vertexLocations = [	1 -100 0 -20   % left anchor
		   	2 -50 0 -20	% left clump weight
			3 0 0 -20		% submerged buoy
			4 50 0 -20	% right clump weight		
			5 100 0 -20	% right anchor
		  ]

%--- Rigid bodies ---%
rigidBody1={
	type = point
	mass = 2000
	V = 1
	vertex = 2
	CD = 1.2
	CM = 1
}

rigidBody2 ={
	type= cylinder
	mass = 2000
	V = 3.5
	vertex = 3
	I = [10e3 10e3]
	h = 2; % cylinder height.
	CD = [1.2 1 0.1]
	CM = [1 1]
}
rigidBody3={
	source = rigidBody1
	vertex = 4
}

%--- Cable types ---%
cableType1={
	diameter = 0.05	
	rho = 3000
	materialModel={
		type = bilinear
		EA = 1e6 % arbitrarily chosen, make softer for more motion. 
	}
	CDn = 1.2;
    CDt = 0.1;
    CMn = 1.0;	
}

%--- Cables ---%
cable1={
	type = 1
	vertex0 = 1
	vertex1 = 2
	IC = {
		type = 'straightLine'
		eps0 = 0.01;
	}
	mesh.N = 10 
}

cable2={
	source = cable1
	vertex0 = 2
	vertex1 = 3
}
cable3={
	source = cable1
	vertex0 = 3
	vertex1 = 4
}

cable4={
	source = cable1
	vertex0 = 4
	vertex1 = 5
}
bc1.vertex = 1;
bc2.vertex = 5;