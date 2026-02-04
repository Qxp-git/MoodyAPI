%% --- Simulation settings
simulation = {
	time = {
		start = 0;
		end =  210;
		dt = 0.001;
	}
	print.dt = 0.01;

	statics = {
		solve= 1;
		maxIter  = 10000;
		timeStep = 0.1;
		relax =1;
	}
};
%% --- Environmental settings
environment = {
	gravity= -9.81;
	waterLevel= 0;
	waterDensity= 1025

	% Set the ground
	ground = {
		level= -320
		type = "springDamp"
		stiffness = 1000000
		dampingCoeff = 1
		damping = 1000
		frictionCoeff =  0.1
		frictionVelocity = 0.05
	};
	% Make waves
	wave = {
		type = "regular"
		amplitude = 2
		period = 7
		phase = 0
		direction = 0
		rampTime = 20
	};
	
	% Some input for moodymarine compatibility
	view = {
		domain =[1000,200]
		groundColor = "tan";
		water  = {
			color = "darkblue";
			resolution = [200,2]; % wave resolution only needed in x-direction for this case
			opacity = 0.6;
			wireframe = 0;
		}
		vertex ={
			color = "black";
			diameter = 0.25;
		}
	}
}

% All points in the system. Only 1,2,4 and 6 are used. 3,5, and 7 are slaves to 1, see hydroBody1.
% For visualization, they are correctly placed here as well, but data is unused.
vertexLocations = [	
	1 	0 			0 			-78.01
	2 	853.87 		0 			-320
	3 	5.2  		0 			-70
	4 	-426.935 	739.4731 	-320
	5  	-2.6 		4.5033 		-70
	6 	-426.935 	-739.4731	-320
	7	-2.6		-4.5033		-70
]

%% --- Cable types	
cableType1 = {
	gamma0 = 77.7066;
	diameter = 0.09;
	rho = 12170;
	CDn = 1.875;
	CDt = 0.86;
	CMn = 0.5;
	CMt = 0;
	materialModel = {
		EA = 384243000;
		xi = 500;
		type = "bilinear";
	}
}

%% --- Cables 

cable1 = {
	vertex0 = 2;
	vertex1 = 3;
	type = 1;
	length = 902.2;
	N = 10;
	IC.type = "catenary";
	view = {
		color = red;
	};
},
cable2={
	vertex0 = 4;
	vertex1 = 5;
	view.color = "green";
	source = "cable1";
}
cable3 = {
	vertex0 = 6;
	vertex1 = 7;
	source = "cable1"
	view.color = "black";
};

%% --- BCs are all anchor points (fixed type is default) --- %%
bc1.vertex = 2;
bc2.vertex = 4;
bc3.vertex = 6;

%% --- Hydrobodies

hydroBody1 = {
	vertex = 1;
	slaves = [
		3 [5.2 0 8.01] 0 [0 0 0 ]
		5 [-2.6 4.5033 8.01] 0 [0 0 0]
		7 [-2.6 -4.5033 8.01] 0 [0 0 0]	
	];
	mass = 8066048;
	constraints = [];
	I = [4229230000,4229230000,164230000];
	meshName = "hywind_20mTower.stl";
	cogInMesh = [0,0,-78.01],
	nlfk = 0;
	hydroData = "./nemoh";
	type = linearIRF;
	IRF = {
		time = 30;
		dt = 0.01;
		save = 1
	};
	view = {
		color = "grey";
		wireframe = 1;
	}
}

%% --- NEMOH INPUT BELOW --- %%
% Info below is only used by moodyPre.exe -nemoh -f <thisInputFile> to generate a Nemoh project.
bem = {
	body = 1;
	type="nemoh"
	output = "nemoh";
	w0 =  0.0628;
	w1 = 4.082;
	nFreqs =  35;
	dir0 = 0;
	dir1 = 0;
	nDirs = 1;
};

% Body specific nemoh-input (used by moodyPre.exe -nemoh)
hydroBody1.bemInput = {
	meshName = "hywind_20mTower.stl";
	keepMesh = 0;
	cogInMesh = [0, 0, -78.01];  % CoG of tower, nacelle and SPAR platform. in mesh coordinates (mesh origin at SWL)
	position = [ 0, 0,	-84.165] % approximate static equilibriae of CoG
};
