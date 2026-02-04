function moodyMovie(field,d,t,dims,varargin)
%% MOODYMOVIE shows how parameter "field" evolves over time t.
% movie is stored as d.caseName_d.name_field.mp4 in the current directory. 
%
% Input: 
%   field: name of field to vierw.
%   d    : cable or rigid body structure. As output from readCase.m
%   
% Optional inputs are:
%   t:    Vector of plot times. Default is 1 frame per saved timestep
%   dims: [i j] (= [1 dim]), i.e. which dimensions to view. 
%         [0 i] means plotting dimension i against the cable coordinate s. 
% Varargin input can be: 
% 'fr'  : framerate [1/s] , or 
% 'dur' : duration [s]
%
% Example:  moodyMovie('v',d,d.t(1:10:end),[0 3],'dur',20)
%
%           Views the time evolution of the z-dimension of cable velocity 
%           along the cable coordinate as a 20 s long movie with frames 
%           every 10th saved timestep of cable structure d.
%           d is the output of d=readCase('outputName)'). See readCase.m 
% 

% Choose dimension:
if nargin < 4 || isempty(dims)
    if isfield(d,'dim')
        dims= [1 d.dim];    % default is x and vertical dimension    
    else
        dims= [1 3];    % default is x and vertical dimension    
    end
end

% Check time: 
if nargin < 3 || ischar(t)
    t=d.t;
end

movName = [d.caseName '_' d.name];

%% Test if input is a rigid body: 
if isfield(d,'type') && strcmp(d.type,'cylinder')
        
    h=0.5*d.height;
    r=0.5*d.diameter;

    corners = [r 0 h; -r 0 h;-r 0 -h; r 0 -h; r 0 h]';
                
    % Compute time indices:
    
    ind = timeIndex(d,t);
    t= d.t(ind);
    R=d.R(ind,:);
    p=d.p(ind,:);
    
    plotVals = cell(length(t));
    Rloc = zeros(3);
    for ii=1:length(t)
        Rloc(:) = R(ii,:);        
        xyz = p(ii,:)'*ones(1,size(corners,2)) + Rloc*corners;        
        plotVals{ii} = xyz(dims,:)';
    end
    
    %   Set global max min for movie
    [maxXY, minXY] = globalMaxMin(plotVals);
    movieInfo.axis = [minXY maxXY];
    movieInfo.mesh = [1 length(corners(1,:))];
    
    movieInfo.title= '';
    movieInfo.x = 'x [m]';
    movieInfo.y = 'z [m]';
    movieInfo.name = movName;
    
else
    %% do for cable

    % Check for adaptive setting
    if iscell(d.s)
        adaptFlag =1;
    else
        adaptFlag = 0;
    end

    % Compute time indices:
    ind = timeIndex(d,t);
    t= d.t(ind);
    plotVals = d.(field)(ind);

    % Scalar valued fields:
    if any(strcmp(field,{'T','eps','epsR'}))
        dims=[0 1];
    end

    % Do for adaptive and nonadaptive meshes:
    if adaptFlag
        mesh = d.elements(ind);
        [meshDensityMax,meshDensityMin] = meshDensity(mesh);
        if dims(1)==0 % use dims(1) = 0 to plot along s.
            sPlot = d.s(ind);
            for ii=1:length(t)
                plotVals{ii} = [sPlot{ii}(:) plotVals{ii}(:,dims(2))];
            end
        else
            for ii=1:length(t)
                plotVals{ii}=plotVals{ii}(:,dims);
            end
        end
    else

        mesh = d.elements;
        if dims(1)==0
            for ii=1:length(t)
                plotVals{ii} = [d.s(:) plotVals{ii}(:,dims(2))];
            end
        else        
            for ii=1:length(t)
                plotVals{ii}=plotVals{ii}(:,dims);            
            end        
        end
    end
    
    
    %% Set movie info for cables:

    [maxXY, minXY] = globalMaxMin(plotVals);
    movieInfo.axis = [minXY maxXY];
    movieInfo.mesh = mesh;


    if adaptFlag
        movieInfo.meshDensity = [meshDensityMin meshDensityMax];
    end


    switch field
        case {'T','eps'}
            movieInfo.x = '$s$ (m)';

            switch field
                case 'T'

                    movieInfo.name = strcat(movName,'_tension');
                    movieInfo.title= 'Tension';

                    if (abs(movieInfo.axis(4))>2e3)
                        movieInfo.y = 'Force (kN)';
                        movieInfo.axis([2 4]) = movieInfo.axis([2,4])/1e3;
                        for ii=1:length(t)
                            plotVals{ii}(:,2) = plotVals{ii}(:,2)/1e3;
                        end
                    else
                        movieInfo.y = 'Force (N)';
                    end
                case 'eps'
                    movieInfo.name = strcat(movName,'_strain');
                    movieInfo.title= 'Strain';
                    movieInfo.y = 'Strain, $\epsilon$ (-)';                
            end

        case 'p'
            movieInfo.title= 'Position';
            labs={'x (m)','y (m)','z (m)'};
            if dims(1) == 0
                movieInfo.x = '$s$ [m]';
            else
                movieInfo.x = labs{dims(1)};
            end
            movieInfo.y = labs{dims(2)};
            movieInfo.name = strcat(movName,'_position');

        case 'v'
            labs={'x','y','z'};
            movieInfo.title= 'Velocity';
            if dims(1) == 0
                movieInfo.x = '$s$ [m]';
            else
                movieInfo.x = ['Velocity, $v_' labs{dims(1)} '$ (m/s)'];
            end
            movieInfo.y = ['Velocity, $v_' labs{dims(2)} '$ (m/s)'];
            movieInfo.name = strcat(movName,'_velocity');

        otherwise
            movieInfo.title= '';
            movieInfo.x = ''; % 'x [m]';
            movieInfo.y = ''; %'z [m]';
            movieInfo.name = strcat(movName,'_movie');
    end

    
end

% Check for framerate or fr name,value pair in varargin:
ii=1;
while ii<length(varargin)
    if strcmp(varargin{ii},'framerate') || strcmp(varargin{ii},'fr')
        movieInfo.fr = varargin{ii+1};
    end
    if strcmp(varargin{ii},'duration') || strcmp(varargin{ii},'dur')
        movieInfo.dur = varargin{ii+1};
    end
    ii=ii+2;
end

saveMovie(t,plotVals,movieInfo)


% * * * * * END OF FILE * * * * * %
