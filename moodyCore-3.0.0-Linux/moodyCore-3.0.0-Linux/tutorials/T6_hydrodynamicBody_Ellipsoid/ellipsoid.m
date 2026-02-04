simulation ={
    time = {
        start = 0;
        end = 100;
        dt = 0.01;
    }
    print.dt  = 0.02;
    % print.format = "ascii"

    statics.solve = 0;
}
environment = {
    waterLevel = 0;
    gravity = -9.81;
    waterDensity = 1025;

    wave = {
        type = 'regular';
        amplitude = 2;
        period = 6;    
        rampTime = 50;
        depth = 100; // 100 m depth simulation
    }
}
vertexLocations = {
    1 [0 0 -2];
    2 [0 0 -12.5];
}

hydroBody1 = {
    type = "linearIRF";
    mass = 133376;
    I = [1.375264e6 1.375264e6 1.341721e6];
    cogInMesh=[0,0,0];
    % volume = 130.12229;
    meshName = "./ellipsoid.stl;"
    hydroData, = "./nemoh";
    nlfk = 1;
    constraints = [1 2 4 5 6];
    vertex = 1;
    IRF={
        time = 50;
        dt = 0.01;
    }
}

component1 = {
    type = "spring";
    stiffness = 0;
    damping = 1200000;
    vertex0 = 1;
    vertex1 = 2;
}

bc1.vertex = 2;

%% ----- Nemoh input ----- %%
bem= {
    body = 1;

    output = "nemoh";
    position = [0,0,0];
    
    w0 = 0.01;  % Starting frequency (rad/s), Lowest frequency of Nemoh solver
    w1 = 20;    % End frequency (rad/s), Highest frequency of Nemoh solver
    nFreqs = 30; % Number of frequencies (-)
    
    dir0 = 0;  % First direction (deg)
    dir1 = 0; % Last direction (deg) -- implies xy-symmetry. 
    nDirs = 1; % Number of directions (-)    
}
hydroBody1.bemInput = {
    
    meshName = "./ellipsoid.stl";
    cogInMesh = [0,0,0];
    position = [0,0,-2];
}