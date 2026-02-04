
% Add path to matlab moody sources
p = fullfile(fileparts(mfilename('fullpath')),'src');
    
addpath(genpath(p)); % only adds if not there


% Create moodyPath variable. 
moodyVersion = '2.0.1';

% Select architecture:
if (ismac)
	arch='Darwin';
	libEnding = '.dylib';
    pathDLM = ':';
elseif (ispc)
	arch='Windows';
	libEnding='dll';
    pathDLM=';';    
else
	arch='Linux';
	libEnding = '.so';
    pathDLM=':';
end

moodyPath=fullfile(p,'..','..','..');

% Set environment to moody directory (for moody.m): 
% NB: This is not always neccessary if moody executables are added to usr/bin    
% Rerunning this script adds to length of system PATH variable. Hence, the check if it is already added. 
isOnPATH = strfind(getenv('PATH'),moodyPath);
if isempty(isOnPATH)
    setenv('PATH',[getenv('PATH') pathDLM fullfile(moodyPath,'build')]);
    setenv('PATH',[getenv('PATH') pathDLM fullfile(moodyPath,'bin')]);
    setenv('PATH',[getenv('PATH') pathDLM fullfile(moodyPath,'lib')]);
end

