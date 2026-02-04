#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 13:57:05 2021

@author: 72516170
"""


class plotTimer(object):

    def __init__(self, t, x, y, line, startInd=0):
        self.tList = t
        self.nt = len(t)
        self.ind = startInd
        self.thisTime = t[self.ind]
        # Store plot data
        self.x = x
        self.y = y
        self.line = line
        if x.ndim == 1:
            self.updateX = 0
        else:
            self.updateX = 1

        if y.ndim == 1:
            self.updateY = 0
        else:
            self.updateY = 1
        print(self.updateX	, self.updateY)

    def skipTo(self, ind):
        self.ind = max(0, min(self.ind, self.nt-1))
        self.update()

    def next(self, event):
        self.ind += 1000  # min(self.nt-1,self.ind+1000) # stay in data bound.
        self.thisTime = self.tList[self.ind]
        if self.updateX == 1:
            self.line.set_xdata(self.x[:, self.ind])
        if self.updateY == 1:
            self.line.set_ydata(self.y[:, self.ind])
        print(self.ind)
        plt.draw()
        # self.update()

    def prev(self, event):
        self.ind = max(0, self.ind-1000)  # stay in data bound.
        self.update()

    def next10(self, event):
        self.ind = min(self.nt-1, self.ind+10)  # stay in data bound.
        self.update()

    def prev10(self, event):
        self.ind = max(0, self.ind-10)  # stay in data bound.
        self.update()

    def toStart(self, event):
        self.ind = 0
        self.update()

    def toEnd(self, event):
        self.ind = self.nt
        self.update()

    def update(self):
        self.thisTime = self.tList[self.ind]
        if self.updateX == 1:
            self.line.set_xdata(self.x[:, self.ind])
        if self.updateY == 1:
            self.line.set_ydata(self.y[:, self.ind])
        print(self.ind)
        plt.draw()
