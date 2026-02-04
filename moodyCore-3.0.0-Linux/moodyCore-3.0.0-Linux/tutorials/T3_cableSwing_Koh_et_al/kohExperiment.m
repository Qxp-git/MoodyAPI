
%--- Simulation settings ---%
simulation = {
    time = {
        start = 0;
        end = 5;
        dt = 1e-5;
    }
    print.dt = 1e-3;    

}

%--- Environmental settings ---%
environment = {
    gravity = -9.81;
    airDensity = 1;
    waterDensity = 1; % cable is "submerged" in air, i.e. no waterLevel is set.
}

%--- Cable type: Neoprene rubber ---%
cableType1 = {
    diameter = 0.025;
    rho = 1430;
    % gamma0 = 5;
    CDn = 1.0;
%   CDt = 0.5;
%   CMn = 1.0;
    materialModel = {
        type = 'bilinear';
        E =3.14e6;   % computes EI and EA for solid cylinder cross-section.
        compressionScale = 1.0; 
        % EA = 1.541343895667492e3; % EA only value
        xi = 4.078725016787873; % Koh damping
    }
}
%----- List of vertices -----%
%                       no.     x       y       z                     
vertexLocations =       {   
                        1     [0       0      0 ];
                        2 [1.805 0 0];                        
                        };
                    
%--- Cables ---%
cable1 = {
    name = 'cable1';
    typeNumber = 1;
    vertex0 = 1; %
    vertex1 = 2; %
    length = 2.022; % (m)
    IC.type = 'catenary'; 
    mesh.N = 10; %
}
%--- Boundary conditions ---%
% Pinned cable end
bc1 = {
    vertex = 1;
    mode = 'fixed';
    % rotationMode = "clamp"   % as console beam.
    % rotValue = [-1 0 0] ; % as console beam.
}

% Dropped cable end
bc2 = {
    vertex = 2;
    mode = 'force';    
    value = [0;0;0]; 
}
