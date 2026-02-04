
%--- Simulation settings ---%
simulation = {
    time = {
        start = 0;      %   [s]     Start time
        end = 20;       %   [s]     End time of simulation
        dt = 1e-4;      %   [s]     Time step size
        % scheme = "RK4"
        %cfl = 0.9;    % use adaptive time step based on max courant number
    }
    print = {
        dt = 1e-2;    % save results every xx time interval
        % format  = binary; % ascii, or binary(default)
    }

    % API ={}
    % numLib = {}
} 

%--- Environmental settings ---%
environment = {
    gravity = -9.81;         % [m/s2]    Gravitational acceleration
    waterLevel = 3;         % [m]       z-coordinate of mean water level
    waterDensity = 1e3;     % [kg/m3]   Density of water
    airDensity = 0.0;       % [kg/m3]   Density of air

    %--- Ground model input  ----%
    ground = {
        level = 0;
        type = 'springDamp';
        % damping = 1e4;
        dampingCoeff = 1;
        frictionCoeff = 0.3;
        frictionVelocity = 0.01;
        stiffness = 3e9;    
        oneWayDamping = 0;     % default is 1, only damping on impact, not in lift. 0 means pure linear damping.                    
    }

    % waves = {}
    % current = {}
    % wind = {}

} % end environment

%---Cable types---%
cableType1 = {
    diameter = 0.0022;
    rho = 7800;
    gamma0 = 0.0818;
    CDn = 2.5;
    CDt = 0.5;
    CMn = 3.8;
    materialModel = {
        type = 'bilinear';
        EA = 1e4; % specific input to material model.
        xi = 2;
    }
}

%--- List of vertices ---%
%                       no.     x       y       z                     
vertexLocations =       {   
                        1     [ 0       0      0 ];
                        2     [ 32.554      0    3.3]
                        };
                    
%----- Cables -----%

cable1 = {
    type = 1;
    vertex0 = 1; %
    vertex1 = 2; %
    length = 33; %
    IC.type = 'catenary'; 
    N =   20;   %
}

%--- Boundary Conditions ---%
bc1 = {
    vertex = 1;    
}
bc2 = {
    vertex = 2;    
    mode = "sine"
    amplitude = [0.2;0;-0.2];   % if scalar it is applied to all dimensions.
    frequency = 0.285714285714286;
    phase = [90;0;0];  % if scalar it is applied to all dimensions. [deg]
    centerValue = [32.554;0;3.3]; % if scalar it is applied to all dimensions.
    rampTime = 7;
}        



