% Simulation settings ---% 
simulation ={
	time= {
		start = 0
		end = 10
		% dt = 1e-2
		cfl = 0.9
	}
	staticSolver.solve = 0;
}

%--- Points ---% 
vertexLocations = [	1 -100 0 0   % left anchor
		   	2 -50 0 0	% left clump weight
			3 0 0 0		% submerged buoy
			4 50 0 0	% right clump weight		
			5 100 0 0	% right anchor
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
component1 = {
	type = "spring"
	vertex0 = 1
	vertex1 = 2
	restLength = 49.5049505 % (m) length at which F is 0. See T5a: 50/(1+0.01) for cable 1.
	stiffness = 202e3    % (N/m) 1/L0*EA from T5a 
}

component2={
	source = component1
	vertex0 = 2
	vertex1 = 3
}

component3={
	source = component1
	vertex0 = 3
	vertex1 = 4
}
component4 = {
	source = component1
	vertex0 = 4
	vertex1 = 5
}

bc1.vertex = 1;
bc2.vertex = 5;
