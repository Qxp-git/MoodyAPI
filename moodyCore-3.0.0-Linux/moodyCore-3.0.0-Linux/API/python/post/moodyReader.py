#!/usr/bin/env python3



''' 
PYTHON MODULE FOR EXECUTING STAND-ALONE MOODY AND POST-PROCESSING THE RESULTS

Uses the subprocess module.
'''

import subprocess

solverName="moody.exe"

## Pass list of moody-style arguments to subprocess and execute moody
def run(file,*args):
    fullList = [solverName,"-f",file]
    fullList.extend(args)
    # subprocess.run(fullList)
    result = subprocess.run(fullList, stdout=subprocess.PIPE).stdout.decode('utf-8')        
    #popen = subprocess.Popen(fullList, stdout=subprocess.PIPE, universal_newlines=True)
    #for stdout_line in iter(popen.stdout.readline, ""):
    #    yield stdout_line 
    #popen.stdout.close()
    #return_code = popen.wait()
    #if return_code:
    #    raise subprocess.CalledProcessError(return_code, fullList)    
    return result

""" READER BEGINS """
import numpy as np
import os
import json
# Python file to post-process and view moody results
# Written by Johannes Palm,Sigma Energy and Marine AB, 20210101

# --- Read results --- #
def read(name):
    return moodyCase(name)


# --- Read json-formatted input file as dictionary. 
def caseSettings(name):
    f=open(name+"/setup.json");
    inputSettings = json.load(f);
    f.close();
    ## Read info.json with file info and lists of objects in results 
    f = open(name+"/info.json");
    fileSettings = json.load(f);
    f.close();

    return inputSettings, fileSettings;

# --- Read input value from setup.txt in results folder.
# Returns string on that line. Not compatible with line-broken vector input.
def readInputKey(name, key):
    
    inpF, = caseSettings(name);
    if key in inpF:
        return inpF[key]
    else:
        return "NOT_FOUND"
        

# --- List properties of a moody results folder (name).
# Returns tuple of: object names,
#                   number of cables,
#                   number of rigid bodies, and
#                   number of components in the case.
def checkCase(name):

    inpF,files = caseSettings(name);
    return files

## ----------------- Moody system ----------------- ##
# Moody results case class.
# Attributes with lists containing all objects in a case.
class moodyCase:
    def __init__(self, resultName):
        inputF,self.info = caseSettings(resultName)
        self.name = resultName
        
        self.t = getAsciiArray(resultName+"/time.dat")
        self.describe()
        # Initialise cables
        self.c=[]
        for n in self.info["cables"]:
            # make full name
            # print('Reading object: ', n)
            # fullName = os.path.join(resultName, n)            
            self.c.append(readCable(resultName,self.info[n]))
        
        # Initialise rigid bodies
        self.b = [];
        for n in self.info['rigidBodies']:            
            self.b.append(readRB(resultName, self.info[n]))

        # Read components:
        self.comp = [];
        for n in self.info["components"]:            
            self.comp.append(componentData(resultName,self.info[n]))


        # Set number of objects
        self.nC = len(self.c)
        self.nB = len(self.b)
        self.nComp = len(self.comp)

        # Compute maximum and minimum tension in all cables:
        self.Tmax = 0.0
        self.Tmin = 1e10
        for cc in self.c:
            self.Tmax = max(self.Tmax, np.amax(np.amax(cc.T)))
            self.Tmin = min(self.Tmin, np.amin(np.amin(cc.T)))
        for cc in self.comp:
            self.Tmax = max(self.Tmax, np.amax(np.amax(cc.T)))
            self.Tmin = min(self.Tmin, np.amin(np.amin(cc.T)))

    # Describe function to browse contents

    def describe(self):
        print("--- Moody case: ",  self.name, ", contains ---")
        print("   --- ", "cables: " , self.info["cables"])
        print("   --- ", "bodies: ", self.info["rigidBodies"])
        print("   --- ", "components: ", self.info["components"])
        print("   --- ", "time: ", "[ "+str(self.t[0])+", "+ str(self.t[len(self.t)-1])+" ]s with "+str(len(self.t))+" entries")
        
## ----------------- Component class data type ----------------- ##
# Attributes:
    # t - time vector
    # Tvec - vector of tension force in the component.
    # T - magnitude of tensionVector.


class componentData:
    def __init__(self, folder,info):
        # Open file and read contents, append columns with T magnitude
        fileName = folder + '/' + info['state']['filename']
        self.name = fileName.split('.dat')[0]        
        forceF = open(fileName)
        data = np.genfromtxt(forceF)
        forceF.close()  # close file        
        self.plotName = self.name
        self.t = data[:, 0]
        self.p0 = data[:,1:4]
        self.p1 = data[:,4:7]
        self.v0 = data[:,7:10]
        self.v1 = data[:,10:13]                
        self.Tvec = data[:, 13:16]        
        if np.shape(data)[1] > 16:
            self.spec = data[:,16:]
        else:
            self.spec = False
        # compute tension magnitude from vector force
        self.T = np.sqrt(np.sum(np.square(self.Tvec), axis=1))
        
    ## Compute relative velocity
    def relativeVelocity(self):
        return (self.v1-self.v0)
    ## Compute length of component
    def length(self):    
        return np.sqrt(np.sum((self.p1-self.p0)**2,axis=1))
    
    def rename(self, name):
        self.name = name
        self.plotName = name

    def endTime(self):
        nt = len(self.t)
        if nt > 0:
            return self.t[nt-1]
        else:
            return -1

## ----------------- Cable mesh ----------------- ##
# Separate data type for cable mesh parameters


class cableMesh:
    def __init__(self):
        self.N = -1
        self.P = -1
        self.nModes = -1
        self.nNodes = -1
        self.s = np.empty(0)
        self.L = -1

## ----------------- Cable data ----------------- ##
# Data type used for cable data but also for probed cables.


class cableData:
    def __init__(self):
        self.name = "noName"
        self.plotName = "noName"
        self.dim = -1
        self.mesh = cableMesh()
        self.sProbes = np.empty(0)
        self.t = np.empty(0)
        self.p = np.empty(0)
        self.Tvec = np.empty(0)
        self.strain = np.empty(0)
        self.T = np.empty(0)
        self.M = np.empty(0)

    def rename(self, name):
        self.name = name
        self.plotName = name

    def endTime(self):
        nt = len(self.t)
        if nt > 0:
            return self.t[nt-1]
        else:
            return -1

    def nQuads(self):
        np = len(self.sProbes)
        if np > 0:
            return self.sProbes
        else:
            return self.mesh.nNodes

## ----------------- Rigid body data ----------------- ##
class rigidBodyData:
    def __init__(self, dim=3):
        self.name = "noName"
        self.plotName = "noName"
        self.dim = dim
        self.t = np.empty(0)
        self.data = np.empty(0)
        self.startState = np.empty(0)
        self.forces = np.empty(0)

    def rename(self, name):
        self.name = name
        self.plotName = name

    def endTime(self):
        return self.t[len(self.t)-1]

    def p(self):
        return self.data[0:3, :]

    def q(self):
        return self.data[3:7, :]

    def rpy(self):
        return self.data[3:6, :]*180.0/np.pi

    def v(self):
        return self.data[7:10, :]

    def w(self):
        return self.data[10:13, :]

    def removeOffset(self):
        self.startState = self.data[:, 0]
        # Dont removw offset on q or rpy
        for i in (0, 1, 2, 7, 8, 9, 10, 11, 12):
            self.data[i, :] -= self.startState[i]

    def Fexc(self):
        return self.forces[0:6, :]

    def Frad(self):
        return self.forces[6:12, :]

    def Fadd(self):
        return self.forces[12:18, :]

    def Frestore(self):
        return self.forces[18:24, :]

    def Fdrag(self):
        return self.forces[24:30, :]

    def Flinear(self):
        return self.forces[30:36, :]


## ---------- Read rigid body ---------- ##
# Get information of rigid body stored as a rigidBodyData type (see above)
def readRB(folder,info):
    rb = rigidBodyData()
    rb.rename(info['state']['filename'].split('.dat')[0])
    rb.t, rb.data = get2dData(folder, info["state"]) #  not counting first time row.
	
    if "forces" in info:
        tOut, rb.forces = get2dData(folder, info["forces"])

    return rb

## ---------- Read cable ---------- ##
# Get information of a cable stored as a cableData type (see above)
def readCable(folder,info):
    # Init empty cable data structure
    c = cableData()    
    # Get name from state file    
    c.name = info['state']['filename'].split('.dat')[0] 
    c.dim = 3 # Always work on 3D values.    
    # Assign mesh variables, always ascii
    c.mesh = getCableMesh(folder+"/"+c.name)

    # Read values:  
    c.t, c.p = get3dData(folder, info['position'])
    t, c.Tvec = get3dData(folder, info['tension'])
    t, c.strain = get2dData(folder,info['strain'])
    # Reduce to norm of tension vector
    c.T = np.sqrt(np.sum(np.square(c.Tvec), axis=1))
    # cData.T = np.sqrt(np.square(cData.Tvec[:,0,:])+np.square(cData.Tvec[:,1,:]))

    try:
        t, c.M = get3dData(folder,info['moment'])
    except:
        print("no moment output in simulation")

    return c


## Store as 2D data matrix with file info: columns, filename and format.
def get2dData(folder,info):
    
    if info['format'] == "binary":
        d = getBinArray(folder+"/"+info['filename'])
    else:
        d = getAsciiArray(folder+"/"+info['filename'])

    nRows = int(len(d)/(info['columns']))
    # Rearrange data size.
    d = d.reshape(nRows, info['columns'], order='C')
    # # Separate into time variable and data variable
    t = d[:, 0]
    d = d[:, 1:]

    return t, d.transpose()

## Store as 3D data matrix with file info: columns, filename and format.
def get3dData(name, info):    
    # Read file into 1D array of doubles    
    t,d = get2dData(name,info);     
    # Reshape to 3D with additional split in 3 pieces.
    I = int((info['columns']-1)/3)
    d2 = d.reshape(I, 3, len(t), order='F')
    return t, d2

## ----------------- Store as 2D data with only knowledge of nLines ----------------- ##
def getData(name,nLines,frmt='bin'):
    # Read file into 1D array of doubles    
    if frmt == 'bin':
        d = getBinArray(name);  # nd is length of d-array
    else: 
        d = getAsciiArray(name);
    
    nd = len(d)
    nCols = nd/nLines
    d = d.reshape(nLines, nCols, order='C')
    t=d[:,0]
    d=d[:,1:]
    return t,d

## ----------------- Reading doubles from file ----------------- ##
def getBinArray(name):
    # Open data file (of doubles)
    f = open(name, "rb")
    d = np.fromfile(f, dtype=np.double)
    f.close()
    return d
## ----------------- Reading ascii files ----------------- ##

def getAsciiArray(name, cols=-1):
    # Open data file (of doubles)
    f = open(name, "r")
    d = np.fromfile(f, dtype=float, sep=" ")
    if cols != -1:        
        d = d.reshape((-1, cols), order='C')
    f.close()
    return d

## ----------------- Read mesh data ----------------- ##
def getCableMesh(name):

    d = getAsciiArray(name+"_mesh.dat")

    cMesh = cableMesh

    # Collect hard-coded format:
    cMesh.N = int(d[1])  # number of elements
    cMesh.nModes = int(d[2])  # number of modes
    
    # nNodes = d[3] # (I really would want this...)
    cMesh.L = d[3]*cMesh.N  # cable length is ds*nElements
    cMesh.P = int(d[4])  # element order

    # Open sPlot file and read s-values
    s = getAsciiArray(name+"_sPlot.dat")
    cMesh.s = s[1:]  # skip initial time value
    cMesh.nNodes = len(cMesh.s)
    return cMesh
    #	return N,P,nModes,nNodes,s


## ---------------------------------------------- ##
##				INTERFACE FUNCTIONS END		      ##
##				SUPPORT FUNCTIONS BELOW		      ##
## ---------------------------------------------- ##

## ---------- Sample information from cable at target times ---------- ##
# Input c is a cable data structure.
# Input tTarget is a list or nparray of target times
# Returns a sampled cable data structure with attribute t =targetTimes
def sampleCable(c, tTarget):

    
    # Limit sampling to range of c.t:
    for tt in range(len(tTarget)):
        if tTarget[tt] < c.t[0] or tTarget[tt] > c.t[-1]:
            print("FATAL ERROR: Trying to sample beyond available time interval")
            
            print("Data t in [" + str(c.t[0]) + ", " + str(c.t[len(c.t)-1]) +"]");
            print("Sampling in [" + str(min(tTarget)) + ", " + str(max(tTarget))+"]");
            exit()
            
    
    # Copy common data:
    c2 = cableData()
    c2.mesh = c.mesh
    c2.sProbes = c.sProbes
    # Assign new sample times:
    c2.sampleTimes = tTarget
    c2.t = tTarget
    # Compute interpolation weights for each time.
    inds, alphas = linterpDG(c.t, c2.sampleTimes)

    # Sample results: (based on first dimension, so transpose results)
    c2.p = linterp(c.p, inds, alphas, 2)
    c2.Tvec = linterp(c.Tvec, inds, alphas, 2)

    # Recompute norm instead of interpolation
    c2.T = np.sqrt(np.sum(np.square(c2.Tvec), axis=1))

    if len(c.M) > 0:
        c2.M = linterp(c.M, inds, alphas, 2)

    return c2

## ---------- Probe information from cable locations ---------- ##
# Input c is a cable data structure.
# Input sTarget is a list or nparray of target positions in cable.
# s is the unstretched coordinate of the cable sTarget \in [0,1]
# Returns a probed cable data structure with attribute sProbes =sTarget
def probeCable(c, sTarget):
    # c is cable data structure.
    # c.mesh is cable mesh class (name,N,P,nModes,nNodes,s)
    # Make sTarget dimensional and send to linear interpolation for weights
    c2 = cableData()
    c2.mesh = c.mesh
    c2.sProbes = np.atleast_1d(sTarget*c.mesh.L)

    # Deal with scalar problem:
    c2.t = c.t
    inds, alphas = linterpDG(c.mesh.s, c2.sProbes)

    # Read position and interpolate result
    # t,d=readM.get3dData(cMesh.name+"_position.dat",cMesh.nNodes,dimensionNumber)
    # cData.t = t
    c2.p = linterp(c.p, inds, alphas).squeeze()
    c2.Tvec = linterp(c.Tvec, inds, alphas).squeeze()

    if c2.Tvec.ndim == 3:
        # Recompute norm instead of interpolation
        c2.T = np.sqrt(np.sum(np.square(c2.Tvec), axis=1)).squeeze()
    else:
        c2.T = np.sqrt(np.sum(np.square(c2.Tvec), axis=0)).squeeze()

    if len(c.M) > 0:
        c2.M = linterp(c.M, inds, alphas).squeeze()

    return c2

## ---------- Linear interpolation factors in a 1D-DG mesh ---------- ##
def linterpDG(x, xT):
    # x is full range of values
    # xT are targets to compute weight for.
    # NB: xT must be sorted
    tol = 1e-10
    nx = len(x)
    nt = len(xT)

    # Index cntr
    xx = 1
    # Assign output
    indT = np.empty(nt, dtype=int)
    alphaT = np.empty(nt)
    #
    isDG = np.min(np.abs(np.diff(x))) < tol

    # Do for each target
    for ii in range(0, nt):
        # find next upper bound which is larger than xT
        while xx < nx-1 and xT[ii] > (x[xx]+tol):
            xx += 1

        # Compute interpolation factor
    alphaT[ii] = (xT[ii]-x[xx-1])/(x[xx]-x[xx-1])

    if isDG and np.abs(alphaT[ii] - 1) < tol and xx < nx-1:
        # If we are at an intermediate boundary (right)
        # use mean value at boundary
        indT[ii] = xx+1
        alphaT[ii] = 0.5
    else:
        # Use the index as is.
        indT[ii] = xx
    return indT, alphaT

## ---------- Interpolate 1d, 2d or 3d data ---------- ##
def linterp(d, inds, alphas, axis=0):

    # interpolate along the first dimension of data array
    ns = len(alphas)

    if axis != 0:
        d = np.swapaxes(d, 0, axis)

    # ----- Do for 3D --- #
    if d.ndim == 3:

        i, j, k = d.shape

        data = np.empty((ns, j, k))

        for ss in range(0, ns):
            indR = inds[ss]
            data[ss, :, :] = d[indR-1, :, :] + \
                alphas[ss]*(d[indR, :, :]-d[indR-1, :, :])

    # ----- Do for 2D --- #
    elif d.ndim == 2:
        i, k = d.shape
        data = np.empty((ns, k))
        for ss in range(0, ns):
            indR = inds[ss]
            data[ss, :] = d[indR-1, :] + alphas[ss]*(d[indR, :]-d[indR-1, :])

    # ----- Do for 1D --- #
    elif d.ndim == 1:
        # for size allocation. NB: Below can prob. be made as one-liner.
        data = alphas
        for ss in range(0, ns):
            indR = inds[ss]
            data[ss] = d[indR-1] + alphas[ss]*(d[indR]-d[indR-1])

    # ----- Cant be done ----- #
    else:
        print("Only dimensions 1-3 are supported for linterp function")
        data = -1

    if axis != 0:
        data = np.swapaxes(data, 0, axis)

    # Return interpolated dataset
    return data

## ----------------- Run as script ----------------- ##
if __name__ == "__main__":

    print("This is Moody Reader")

# DONE
