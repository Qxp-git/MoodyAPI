% script for case setup %

simulation.time.start  = 0;
simulation.time.end = 10;
simulation.time.cfl = 0.9;
simulation.time.scheme = 'RK3';

simulation.print.dt = 0.02;

%% extra quadpoints used for increased ground contact performance.
simulation.numLib.qPointsAdded = 10;

%-------------------------------------------------------------------------%
%--------------------------- Ground model input  -------------------------%
%-------------------------------------------------------------------------%
environment={
    waterLevel = 0;         % [m]       z-coordinate of mean water level
    waterDensity = 1000.0;     % [kg/m??]   Density of water
    airDensity = 1.0;         % [kg/m??]   Density of air

    ground.type = 'springDamp';
    ground.level = -0.9;
    ground.dampingCoeff = 1.0;
    ground.frictionCoeff = 0.1;
    ground.vc = 0.01;
    ground.stiffness = 300.0e6;
}
%-------------------------------------------------------------------------%
%---------------------------- Type definition ----------------------------%
%-------------------------------------------------------------------------%
cableType1.diameter = 0.005;
cableType1.gamma0 = 0.15;
cableType1.CDn = 1.5;
cableType1.CDt = 0.5;
cableType1.CMn = 1.5;
cableType1.materialModel.type = 'bilinear';
cableType1.materialModel.EA =  1.0e4;
        
%-------------------------------------------------------------------------%
%------------------------------- Geometry --------------------------------%

vertexLocations = {
    1    [-3.4587   5.9907  -0.9];
    2    [-0.1362   0.2360   0.0];
    3    [-3.4587  -5.9907  -0.9];
    4    [-0.1362  -0.2360   0.0];
    5    [ 6.9175   0.0      -0.9];
    6    [ 0.2725   0.0      0.0];
    7    [ 0 0 0];
    };
                   
                         
%----- Object definitions -----%
cable1.typeNumber = 1;
cable1.vertex0 = 1; %
cable1.vertex1 = 2; %
cable1.length = 6.95; % 
cable1.IC.type = 'CatenaryStatic';
cable1.mesh.N = 10; % 
% % 
cable2.source=cable1;
cable2.vertex0 = 3; %
cable2.vertex1 = 4; %
% %
cable3.source=cable1;
cable3.vertex0 = 5; %
cable3.vertex1 = 6; %

%-------------------------------------------------------------------------%
%                           Boundary conditions                           %
%-------------------------------------------------------------------------%

bc1.vertex = 1;
bc1.type = 'dirichlet';
bc1.mode = 'fixed';
%
bc2.source = bc1;
bc2.vertex = 3;
% 
bc3.source = bc1;
bc3.vertex = 5;

bc4.vertex = 7;
bc4.type = 'dirichlet';
bc4.mode = 'rigidBody';
bc4.inputDoFs = 6; % could be 7 as well
bc4.slaves = [2 4 6];
bc4.slavePositions = [
                        [-0.1362   0.2360   0.0]
                       [-0.1362   -0.2360   0.0];
                        [ 0.2725   0.0      0.0]
                      ];
               
% --- API conectivitity --- %
simulation.API.bcNames = {'bc4'};
simulation.API.reboot= 'no';
simulation.API.syncOutput = 0; 
simulation.API.staggerTimeFraction= 0.5;

% ===== END OF FILE ===== %
