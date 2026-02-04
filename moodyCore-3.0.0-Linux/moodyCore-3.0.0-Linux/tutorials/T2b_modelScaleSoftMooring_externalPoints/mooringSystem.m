%% Moody model file for 3 catenary chains
% The experimental setup is that of Paredes et al. (2016)
% which was later used for numerical validated of Moodys coupling to
% OpenFOAM in Palm et al. (2016)
%
% 
% G. Paredes, J. Palm, and C. Eskilsson, L. Bergdahl and F. Taveira-Pinto,
% Experimental investigation of mooring configurations for wave energy converters
% Int. J. of Marine Energy 15. 56-67 (2016)
% 
% J. Palm, C. Eskilsson, G. Paredes and L. Bergdahl,
% Coupled mooring analysis for floating wave energy converters using CFD: Formulation and validation,
% Int. J. of Marine Energy, 16. 83-99 (2016)

environment = {
     waterLevel = 0;          	% [m]               z-coordinate of mean water level
     waterDensity = 1000.0;     	% [kg/m3]      Density of water
     airDensity = 1.0;         	% [kg/m3]      Density of air
     gravity = -9.81;              % [m/s2]       

     % waves = {}

     % current = {}

     % wind = {}

     ground = {
          type = 'springDamp';
          level = -0.9;
          damping = 7000;
          frictionCoeff = 0.1;
          frictionVelocity = 0.01;
          stiffness = 3e8;
     }
};

simulation = {
     time = {
          start  = 0;
          end = 10;
          cfl = 0.9;
          scheme = 'RK3';
     }
     print.dt = 0.001; % output interval.
     
     % --- API settings --- %
     API = {
          output = "moodyResults"
          bcNames = ["bc4","bc5","bc6"] % with mode externalPoint
          staggerTimeFraction = 0.5
          syncOutput = 1
          reboot = 'yes'  
     }

     numLib = {
          
          % extra quadpoints used for increased ground contact performance.
          % it makes the difference between stable and non-stable results. 
          qPointsAdded = 10;
     }

     % To remove initial fluctuations due to very stiff ground
     statics = {
          relax = 1;
     }
}


%--- Cable type ---%
cableType1 = {
     diameter = 0.005;
     gamma0 = 0.15;
     CDn = 1.5;
     CDt = 0.5;
     CMn = 1.5;
     materialModel = {
          type = 'bilinear';
          EA =  1.0e4;
     }
}
%--- Points ---%
vertexLocations = {
                       1    [-3.4587   5.9907  -0.9];
                       2    [-0.1362   0.2360   0.0];
                       3    [-3.4587  -5.9907  -0.9];
                       4    [-0.1362  -0.2360   0.0];
                       5    [ 6.9175   0.0      -0.9];
                       6    [ 0.2725   0.0      0.0];                       
                  };
                   
%--- Cables ---%
cable1 = {
     typeNumber = 1;
     vertex0 = 1; %
     vertex1 = 2; %
     length = 6.95; % 
     IC.type = 'catenary';
     mesh.N = 10; % 
} 
cable2 = {
     source=cable1; % Copy remaining info from cable1.
     vertex0 = 3; 
     vertex1 = 4; 
}
cable3 = {
     source=cable1;
     vertex0 = 5; 
     vertex1 = 6;
}

%--- Boundary Conditions ---%
% Three anchors defined by vertexLocations
bc1.vertex = 1;
bc2.vertex = 3;
bc3.vertex = 5;

% Same sinusoidal motion on all three fairleads. 
bc4 = {
     mode = 'externalPoint';
     vertex = 2;
     inDofs = 3;
}
bc5= {
     mode = 'externalPoint';
     vertex = 4;
     inDofs = 3;
}
bc6 = {
     mode = 'externalPoint';
     vertex = 6;
     inDofs = 3;
}

% ===== END OF FILE ===== %
