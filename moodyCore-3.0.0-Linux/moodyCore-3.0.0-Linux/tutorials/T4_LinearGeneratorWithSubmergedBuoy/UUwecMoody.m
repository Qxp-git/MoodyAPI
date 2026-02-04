%--- Simulation settings ---%
simulation = {
    time = {
        start = 0;      %   [s]     Start time
        end = 120;      %   [s]     End time of simulation (20 wave periods)
        dt =1e-2;     %   [s]     Time step size
        cfl = 0.9;	% use time-step control based on CFL condition of cables.
    }
    print.dt = 1e-2;    % save results every xx time interval

    statics = {
        solve = 1;     
        maxIter = 20000;   
        relax = 1;
        relaxIter = 10000;
        relaxCFL = 0.2;
    }
}
environment = {
    gravity = -9.81;            % [m/s2] 
    waterLevel = 0;         % [m]       z-coordinate of mean water level.
    waterDensity = 1025;     % [kg/m3]   Density of water
    airDensity = 0;         % [kg/m3]   Density of air
    
    ground.level = -75;

    wave = {
        type = 'regular';
        amplitude = 1;
        period  = 6;
        phase = 0;
        rampTime = 30;
        depth = 75;   
    }
}


%----- List of vertices -----%  no.     x       y       z                      
vertexLocations = {
                        1     [0 0 -5.25]; 	% buoy cog in bem-file.
                        2     [0 0 -6.3]; 	% upper attachment to buoy. Value over-written by rb1.slaves
                        3     [0 0 0]; 		% unused
                        4     [0 0 -71.4]; 	% upper translator point. Value overwritten by rb2.slaves
                        5     [0 0 -72.3]; 	% translator position (-70+1.8+0.9). translator cog.                            
                        };
                    
%----- Object definitions -----%
%--- Cable types ---%
cableType1 = {
    diameter = 0.04;
    rho = 5204      % [kg/m3] 1025 is a neutrally buoyant line. 
                    % 7800 for solid steel
    CDn = 1.0;
    CDt = 0.1;
    materialModel ={
        type = 'bilinear';
        E = 1.55e10;          % will compute bending stiffness according to area (pi d²/4). use separate EI, EA inputs to specify independent values
        % EA = 1.95e7;        % Uncomment for use without bending stiffness. (If .E input is commented)
        xi = 1.71e3;          % linear internal damping factor (Ns)
        compressionScale = 0.01;    
    }
}


% Cable definition: Comment if simple spring component should be used instead.
cable1 = {
    typeNumber = 1;
    vertex0 = 2;
    vertex1 = 4;
    IC={
        type = 'straightLine';
        eps0 = 0.004; % pretension to match         
    }
    length = 64.5;
    mesh.N = 5;
}
% Comment cable and uncomment component to run with equivalent spring instead of cable
%component1 = {
%    type = "spring"
%    vertex0 = 2
%    vertex1 = 4
%    stiffness = [300e3]
%    damping = [26.341] 
%    restLength = 64.5; 
%    allowCompression = 0   
%}

% --- Buoy --- %
rigidBody1 = {
    vertex = 1;
    type = 'cylinder';
    h = 2.12;
    mass = 5000; % kg
    V = 10; % m3
    I = [6292.6 8288.5]; % solid cylinder values
    CM = [1,1]
    CD = [1,0.8,0.01] % normal-direction, value for lid (symmetry axis direction), and slip drag coeff for torque and vertical motion only.
    slaves =[2 [0 0 -1.05] 0 [0 0 0]];  % relative to cog of body (vertex 1) in body coordinates.
}

%  ---  Translator --- %
rigidBody2= {
    vertex = 5;  
    type = 'translator';
    mass = 5000;
    V = 1; % not used due to sealed
    midPoint = [0 0 -72.3]; % defines center point for strokelength and end-stop measurement. Fixed in space.
    direction = [0 0 1];
    slaves = [4 [0 0 0.9] 0 [0 0 0]]; % position of vertex 4 relative to rigidBody2 (vertex5) in rb2 coordinates. 

    % --- Wec properties --- %
    strokeLength = 1.2; % m, single amplitude of motion
    endStopStiffness =  776e3; % N/m stiffness
    % endStopDamping = 139172; % critical damping.
    endStopLength = 0.6;       % m  
    endStopFullCompressionStiffness = 776e4; % 10 times stiffer when fully compressed. Infinite compression allowed 
    sealed = 1; % switch to turn off ambient water forces.
    rhoSeal = 0; % no net buoyancy. translator in vaccuum.
    damping =59e3; % linear damping factor applied to 1D motion.
    printForces =1 % print force decomposition
}
