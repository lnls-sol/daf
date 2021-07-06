#!/usr/bin/env python3
"""Describe the experiment inputs"""

import argparse as ap
import sys
import os
import dafutilities as du
import numpy as np
import daf

epi = '''
Eg:
    daf.expt --Material Si --Energy 8000
    daf.expt -m Si -e 8000
    daf.expt -s x+
    daf.expt -i 1 0 0 -n 0 1 0
    '''

parser = ap.ArgumentParser(formatter_class=ap.RawDescriptionHelpFormatter, description=__doc__, epilog = epi)

parser.add_argument('-m', '--Material', metavar='samp', type=str, help='Sets the material that is going to be used in the experiment')
parser.add_argument('-p', '--Lattice_parameters', metavar=('a', 'b', 'c', 'alpha', 'beta', 'gamma '), type=float, nargs=6, help='Sets lattice parameters, must be passed if defining a new material')
parser.add_argument('-i', '--IDir', metavar=('x', 'y', 'z'), type=float, nargs=3,help='Sets the reflection paralel to the incident beam')
parser.add_argument('-n', '--NDir', metavar=('x', 'y', 'z'), type=float, nargs=3,help='Sets the reflection perpendicular to the incident beam')
parser.add_argument('-r', '--RDir', metavar=('x', 'y', 'z'), type=float, nargs=3,help='Sets the reference vector')
parser.add_argument('-s', '--Sampleor', metavar='or', type=str,help='Sets the sample orientation at Phi axis')
parser.add_argument('-e', '--Energy', metavar='en', type=float, help='Sets the energy of the experiment (eV), wavelength can also be given (angstrom)')

args = parser.parse_args()
dic = vars(args)


dict_args = du.read()

for j,k in dic.items():
    if j in dict_args and k is not None:
        dict_args[j] = str(k)
du.write(dict_args)


if args.Lattice_parameters:
    dict_args['lparam_a'] = str(args.Lattice_parameters[0])
    dict_args['lparam_b'] = str(args.Lattice_parameters[1])
    dict_args['lparam_c'] = str(args.Lattice_parameters[2])
    dict_args['lparam_alpha'] = str(args.Lattice_parameters[3])
    dict_args['lparam_beta'] = str(args.Lattice_parameters[4])
    dict_args['lparam_gama'] = str(args.Lattice_parameters[5])
    du.write(dict_args)


dict_args = du.read()

if args.Material:
    Uw = dict_args['U_mat'].split(',')


    U1 = [float(i) for i in Uw[0].strip('][').split(' ') if i != '']
    U2 = [float(i) for i in Uw[1].strip('][').split(' ') if i != '']
    U3 = [float(i) for i in Uw[2].strip('][').split(' ') if i != '']
    U = np.array([U1, U2, U3])
    mode = [int(i) for i in dict_args['Mode']]

    exp = daf.Control(*mode)
    exp.set_material(dict_args['Material'], float(dict_args["lparam_a"]), float(dict_args["lparam_b"]), float(dict_args["lparam_c"]), float(dict_args["lparam_alpha"]), float(dict_args["lparam_beta"]), float(dict_args["lparam_gama"]))
    exp.set_exp_conditions(en = float(dict_args['Energy']))
    exp.set_U(U)
    UB = exp.calcUB()
    dict_args['U_mat'] = str(U[0]) + ',' + str(U[1]) + ',' + str(U[2])
    dict_args['UB_mat'] = str(UB[0]) + ',' + str(UB[1]) + ',' + str(UB[2])
    du.write(dict_args)


log = sys.argv.pop(0).split('command_line/')[1]

for i in sys.argv:
    log += ' ' + i

os.system("echo {} >> Log".format(log))

if dict_args['macro_flag'] == 'True':
    os.system("echo {} >> {}".format(log, dict_args['macro_file']))
