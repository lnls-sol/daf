#!/usr/bin/env python3
"""Perform a scan from a csv file generated by daf.scan"""

import sys
import os
import subprocess
import daf
import numpy as np
import dafutilities as du
import scan_daf as sd
import pandas as pd
import yaml
import argparse as ap
import h5py

# Py4Syn imports
import py4syn
from py4syn.utils import scan as scanModule
from py4syn.utils.scan import setFileWriter, getFileWriter, getOutput, createUniqueFileName

# scan-utils imports
from scan_utils.hdf5_writer import HDF5Writer
from scan_utils import cleanup, die
from scan_utils import Configuration, processUserField, get_counters_in_config
from scan_utils.scan_pyqtgraph_plot import PlotScan
from scan_utils.scan_hdf_plot import PlotHDFScan
from scan_utils import PlotType
from scan_utils import WriteType
from scan_utils import DefaultParser
from scan_utils.scan import ScanOperationCLI

epi = '''
Eg:
    daf.rfscan my_scan -t 0.01

    '''

parser = ap.ArgumentParser(formatter_class=ap.RawDescriptionHelpFormatter, description=__doc__, epilog=epi)
parser.add_argument('file_name', type=str, help='Perform a scan from the file generated by daf.scan')
parser.add_argument('-cf', '--configuration', type=str, help='choose a counter configuration file', default='default')
parser.add_argument('-t', '--time', metavar='', default=0.01, type=float, help='Acquisition time in each point in seconds. Default is 0.01s.')
parser.add_argument('-o', '--output', help='output data to file output-prefix/<fileprefix>_nnnn', default='scan_daf')
parser.add_argument('-s', '--sync', help='write to the output file after each point', action='store_true')
parser.add_argument('-x', '--xlabel', help='motor which position is shown in x axis (if not set, point index is shown instead)', default='points')
parser.add_argument('-np', '--no-plot', help='Do not plot de scan', action='store_const', const=PlotType.none, default=PlotType.pyqtgraph)
parser.add_argument('-cw', '--close-window', help='Close the scan window after it is done', default=False, action='store_true')

args = parser.parse_args()
dic = vars(args)
dict_args = du.read()
du.log_macro(dict_args)

scan_points = pd.read_csv(args.file_name)
mu_points = [float(i) for i in scan_points["Mu"]] # Get only the points related to mu
eta_points = [float(i) for i in scan_points["Eta"]] # Get only the points related to eta
chi_points = [float(i) for i in scan_points["Chi"]] # Get only the points related to chi
phi_points = [float(i) for i in scan_points["Phi"]] # Get only the points related to phi
nu_points = [float(i) for i in scan_points["Nu"]] # Get only the points related to nu
del_points = [float(i) for i in scan_points["Del"]] # Get only the points related to del

if du.PV_PREFIX == "EMA:B:PB18":
    data = {'huber_mu':mu_points, 'huber_eta':eta_points, 'huber_chi':chi_points,
            'huber_phi':phi_points, 'huber_nu':nu_points, 'huber_del':del_points}
else:
    data = {'sol_m3':mu_points, 'sol_m5':eta_points, 'sol_m2':chi_points,
            'sol_m1':phi_points, 'sol_m4':nu_points, 'sol_m6':del_points}

motors = [i for i in data.keys()]

with open('.points.yaml', 'w') as stream:
    yaml.dump(data, stream, allow_unicode=False)

args = {'configuration': dict_args['default_counters'].split('.')[1], 'optimum': None, 'repeat': 1, 'sleep': 0, 'message': None, 
'output': args.output, 'sync': True, 'snake': False, 'motor': motors, 'xlabel': args.xlabel, 
'prescan': 'ls', 'postscan': 'pwd', 'plot_type': args.no_plot, 'relative': False, 'reset': False, 'step_mode': False, 
'points_mode': False, 'start': None, 'end': None, 'step_or_points': None, 'time': [[args.time]], 'filename': '.points.yaml'}

scan = sd.DAFScan(args, close_window=dic['close_window'])
scan.run()
