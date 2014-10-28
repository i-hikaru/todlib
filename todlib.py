#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import datetime as dt
import pandas as pds
import glob
import os.path
import pytz

__version__ = '0.1.1'

class TOD(object):
    def __init__(self, filename, usecols=None):
        self._filename = filename
        self._usecols  = usecols
        self._data     = np.genfromtxt(filename, skip_footer=1, usecols=usecols)
        self._ts       = np.array(self._data[:,0])
        self._vals     = np.array(self._data[:,1:])
    def ts(self, skip=1):
        return self._ts[::skip]
    def dates(self, skip=1, tz=pytz.timezone('Asia/Tokyo')):
        return np.array([dt.datetime.fromtimestamp(t, tz) for t in self.ts(skip)])
    def vals(self, skip=1):
        return self._vals[::skip]
    def get_channel_vals(self, channel, skip=1):
        return self._vals[:,channel:skip]

def gentod(filename, usecols=None, skip=1, colslabel=None):
    tod = TOD(filename, usecols=usecols)
    return pds.DataFrame(tod._vals[::skip], index=tod.dates(skip), columns=colslabel)
def gentod_all(dirname, usecols=None, skip=1, colslabel=None, extension='dat'):
    todAll = []
    for f in sorted(glob.glob('%s/*.%s' % (dirname, extension))):
        todAll.append(gentod(f, usecols=usecols, skip=skip, colslabel=colslabel))
    return pds.concat(todAll, axis=0)
