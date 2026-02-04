#!/usr/bin/env python

import numpy as np
import moodyReader as mr
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.figsize'] = 16, 9
dimensionNumber = 3

# globally defined color order:
defaultColors = ['k', 'r', [0, 0, 0.8], [0, 0.8, 0],
                 [0.8, 0, 0.8], [0.8, 0, 0.8], [0, 0.8, 0.8]]
cmap = plt.get_cmap("tab10")

# Plot case provides a number of typically instructive plots of a moody results case.


def plotCase(name, **kwargs):
    if isinstance(name, str):
        res = mr.moodyCase(name)
    else:
        res = name
        name = res.name

    plotIt = False
    if "save" in kwargs:
        plotIt = True        

    if res.nB > 0:
        f = plt.figure()
        ax = plt.gca()
        for bb in res.b:
            ax.plot(bb.t, bb.p()[2, :], linewidth=1.5, label=bb.name)

        frmtTimePlot(ax, [res.b[0].t[0], res.b[0].endTime()], "Heave (m)")
        if plotIt:
            plt.tight_layout()
            f.savefig(name+"/heaveMotion.png", dpi=300)
    if res.nC > 0 or res.nComp:
        f = plt.figure()
        ax = plt.gca()

        # Check case for scale of tension.
        print ("max force ", res.Tmax)
        if res.Tmax > 1e3:

            yScale = 1e3
            yUnit = "(kN)"
        else:
            yScale = 1.0
            yUnit = "(N)"

        ii = 0
        for cc in res.c:
            ax.plot(cc.t, cc.T[0, :]/yScale, linewidth=1.5,
                    color=cmap(ii), label=cc.name+"$_{s=0}$")
            m, n = cc.T.shape
            ax.plot(cc.t, cc.T[m-1, :]/yScale, '--', linewidth=1.5,
                    color=cmap(ii), label=cc.name+"$_{s=1}$")
            ii += 1
        for cc in res.comp:
            ax.plot(cc.t, cc.T/yScale, '-',linewidth=1.5,
                    color=cmap(ii), label=cc.name)
            ii += 1

        if res.nC > 0:
            frmtTimePlot(
                ax, [res.c[0].t[0], res.c[0].endTime()], "Tension "+yUnit)
        else:
            frmtTimePlot(
                ax, [res.comp[0].t[0], res.comp[0].endTime()], "Tension "+yUnit)

        if plotIt:
            plt.tight_layout()
            f.savefig(name+"/tension.png", dpi=300)

    if res.nC > 0:

        if "envelopeResolution" in kwargs:
            envRes = kwargs.pop("envelopeResolution")
        else:
            envRes = 10
        # Plot cables position at time.
        f = plt.figure()
        ax2 = plt.subplot(111, projection='3d')
        ii = 0
        for cc in res.c:
            ts = np.linspace(cc.t[0], cc.endTime(), envRes)
            for tt in ts:
                ax2 = plotCablePosition(cc, tt, axis=ax2, color=cmap(
                    ii), label=cc.name, threeD=True)
            ii += 1
        if plotIt:
            plt.tight_layout()
            f.savefig(name+"/cableEnvelope.png", dpi=300)

    plt.show()
    return res

# Plot position at time list t in 3d view and return the sampled cable info. Use axis=ax for adding to existing plot.
# By default a newplot is rendered. Other plot-command kwargs apply.


def plotCablePosition(c, t, **kwargs):

    # Plot the position of the cables in 3d or 2d:
    # Keyword specially treated: axis
    if 'axis' in kwargs:
        ax = kwargs.pop('axis')  # get value and remove key
    elif 'threeD' in kwargs:
        ax = plt.subplot(111, projection='3d')
    else:
        ax = plt.gca()

    # Sample cable at time t
    ct = mr.sampleCable(c, np.array([t]))
    p = ct.p

    if 'threeD' in kwargs:
        kwargs.pop('threeD')
        for ii in range(0, len(ct.t)):
            ax.plot(p[:, 0, ii], p[:, 1, ii],
                    p[:, 2, ii], linewidth=1.5, **kwargs)
    else:
        for ii in range(0, len(ct.t)):
            ax.plot(p[:, 0, ii], p[:, 2, ii], linewidth=1.5, **kwargs)

    return ax

## ---------- Collect color at index ind ----------- ##


def getColor(ind):

    N = len(defaultColors)
    ind -= N * (ind//N)
    print(ind)
    return defaultColors[ind]


## ---------- Plot a rigid body ---------- ##
def plotBody(case, name="rigidBody1"):

    # Read body
    rb = mr.readRB(case+"/"+name)

    # Plot body position
    plotBodyPosition(rb)
    plt.figure()
    # Plot body rotation
    plotLinearBodyRotation(rb)

    return rb

## ---------- Shorthand function for formatting a time series plot ---------- ##


def frmtTimePlot(ax, lims, ylabel, ncols=-1):

    ax.grid()  # turn on grid
    # Collect number of lines in plot and set legend size as default
    if ncols == -1:
        ncols = len(ax.lines)

    # if n-entries are larger than 4, then expand the column.
    if ncols >= 4:
        # Make legend above plot, centered
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102),
                  loc='lower center', borderaxespad=0.,
                  ncol=ncols, fontsize="small",
                  mode="expand")
    else:
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102),
                  loc='lower center', borderaxespad=0.,
                  ncol=ncols, fontsize="small")

    ax.set_xlim(xmin=lims[0], xmax=lims[1])
    # If specified, also set y-limits.
    if len(lims) == 4:
        ax.set_ylim(ymin=lims[2], ymax=lims[3])

    # Set current axis
    plt.sca(ax)
    # Make axis labels
    plt.xlabel('Time (s)')
    plt.ylabel(ylabel)


def frmtPlot(ax, **kwargs):

    ax.grid()  # turn on grid
    # Collect number of lines in plot and set legend size as default
    if "ncols" in kwargs:
        ncols = kwargs.pop("ncols")
    else:
        ncols = len(ax.lines)

    if "labelLines" in kwargs:
        ls = kwargs.pop("labelLines")
        ax.legend(ls)
        ncols = len(ls)

    # if n-entries are larger than 4, then expand the column.
    if ncols >= 4:
        # Make legend above plot, centered
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102),
                  loc='lower center', borderaxespad=0.,
                  ncol=ncols, fontsize="small",
                  mode="expand")
    else:
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102),
                  loc='lower center', borderaxespad=0.,
                  ncol=ncols, fontsize="small")


## ---------- Plot rigid body motion history ---------- ##
def plotBodyPosition(rb, inds=[0, 1, 2], colors=['k', 'r', 'b'], ax=None):
    if ax is None:
        ax = plt.gca()
    for ii in range(0, len(inds)):
        ax.plot(rb.t, rb.p()[inds[ii], :], colors[ii], linewidth=1.2,
                label=rb.plotName+'$^{(\eta_'+str(inds[ii]+1)+')}$')

    frmtTimePlot(ax, [rb.t[0], rb.endTime()], 'Position (m)')

    return ax

## ---------- Plot rigid body motion history ---------- ##


def plotLinearBodyRotation(rb, inds=[0, 1, 2], colors=['k', 'r', 'b'], ax=None):
    if ax is None:
        ax = plt.gca()

    for ii in range(0, len(inds)):
        ax.plot(rb.t, rb.rpy()[inds[ii], :], colors[ii], linewidth=1.2,
                label=rb.plotName+'$^{(\eta_'+str(inds[ii]+4)+')}$')

    frmtTimePlot(ax, [rb.t[0], rb.endTime()], 'Rotation (deg)')

    return ax

# plot2d(x,y,ax=None,**kwargs)


def plot2d(x, y, **kwargs):
    # Moody keyword specially treated: axis
    if 'axis' in kwargs:
        ax = kwargs.pop('axis')  # get value and remove key
    else:
        ax = plt.gca()

    # Moody keyword specially treated: color
    if "color" in kwargs:
        col = kwargs.pop('color')  # get value and remove key
    else:
        col = getColor(len(ax.lines))

    ax.plot(x, y, color=col, **kwargs)

    return ax


## ---------- Plot tension in cable for all probes ---------- ##
def plotTension(c, colors=['k', 'r', 'b']):

    # Check if c is a cable name:
    if isinstance(c, str):
        c = mr.readCable(c)
        c = mr.probeCable(c, np.array([0, 1]))

    ax = plt.gca()

    # Change scale based on size of input
    if np.max(c.T) > 1e3:
        yScale = 1.0/1e3
        yLab = 'Tension (kN)'
    else:
        yScale = 1.0
        yLab = 'Tension (N)'

    # Plot for all probes:
    for ss in range(0, len(c.sProbes)):
        ax.plot(c.t, c.T[ss, :]*yScale, colors[ss], linewidth=1.2,
                label=c.plotName+'$^{('+str(c.sProbes[ss]/c.mesh.L)+')}$')

    frmtTimePlot(ax, [c.t[0], c.endTime()], yLab)

    return ax


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:

        name = sys.argv[1]
        
        if len(sys.argv) > 2 and sys.argv[2] == "save":            
            plotCase(name, save="yep")
        else:
            plotCase(name)

    else:
        print("Please provide case name to plot. Usage: moodyPlt.py <resultFolderName>")

    plt.show()
