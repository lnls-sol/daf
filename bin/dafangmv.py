#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse as ap
import sys
import os
import daf
import numpy as np
import dafutilities as du



doc = """

Move by setting a HKL or by a given diffractometer angle

"""

epi = "\n Eg: \n daf.move -mv 1 0 0, \n daf.move --Eta 15 -Del 30"


parser = ap.ArgumentParser(description=doc, epilog=epi)

parser.add_argument('-m', '--Mu', metavar='', type=float, help='Constrain naz, default: 0')
parser.add_argument('-e', '--Eta', metavar='', type=float, help='Constrain naz, default: 0')
parser.add_argument('-c', '--Chi', metavar='', type=float, help='Constrain naz, default: 0')
parser.add_argument('-p', '--Phi', metavar='', type=float, help='Constrain naz, default: 0')
parser.add_argument('-n', '--Nu', metavar='', type=float, help='Constrain naz, default: 0')
parser.add_argument('-d', '--Del', metavar='', type=float, help='Constrain naz, default: 0')
# parser.add_argument('-v', '--verbosity', action='store_true', help='Show full output')

args = parser.parse_args()
dic = vars(args)



with open('Experiment', 'r+') as exp:
 
    lines = exp.readlines()


 

    for i, line in enumerate(lines):
        for j,k in dic.items():
            

 

            if line.startswith(str(j)):
                if k != None:
                    lines[i] = str(j)+'='+str(k)+'\n'
          
            exp.seek(0)
            


 

    for line in lines:
        exp.write(line)


     
dict_args = du.dict_conv()
 
        
def ret_list(string):
    
    return [float(i) for i in string.strip('][').split(', ')]


Uw = dict_args['U_mat'].split(',')


U1 = [float(i) for i in Uw[0].strip('][').split(' ') if i != '']
U2 = [float(i) for i in Uw[1].strip('][').split(' ') if i != '']
U3 = [float(i) for i in Uw[2].strip('][').split(' ') if i != '']
U = np.array([U1, U2, U3])



mode = [int(i) for i in dict_args['Mode']]  
idir = ret_list(dict_args['IDir'])
ndir = ret_list(dict_args['NDir'])

exp = daf.Control(*mode)
exp.set_exp_conditions(idir = idir, ndir = ndir, en = float(dict_args['Energy']), sampleor = dict_args['Sampleor'])
exp.set_material(dict_args['Material'])
exp.set_U(U)
hklnow = exp.calc_from_angs(float(dict_args["Mu"]), float(dict_args["Eta"]), float(dict_args["Chi"]), float(dict_args["Phi"]), float(dict_args["Nu"]), float(dict_args["Del"]))
hklnow = list(hklnow)
pseudo = exp.calc_pseudo(float(dict_args["Mu"]), float(dict_args["Eta"]), float(dict_args["Chi"]), float(dict_args["Phi"]), float(dict_args["Nu"]), float(dict_args["Del"]))

pseudo_dict = {'alpha':pseudo[0], 'qaz':pseudo[1], 'naz':pseudo[2], 'tau':pseudo[3], 'psi':pseudo[4], 'beta':pseudo[5], 'omega':pseudo[6], 'hklnow':hklnow}


with open('Experiment', 'r+') as exp:
 
    lines = exp.readlines()


 

    for i, line in enumerate(lines):
        for j,k in pseudo_dict.items():
            

 

            if line.startswith(str(j)):
                    lines[i] = str(j)+'='+str(k)+'\n'
          
            exp.seek(0)
            
          


    for line in lines:
        exp.write(line)

    
log = sys.argv.pop(0).split('command_line/')[1]    

for i in sys.argv:
    log += ' ' + i

os.system(f"echo {log} >> Log")

if dict_args['macro_flag'] == 'True':
    os.system(f"echo {log} >> {dict_args['macro_file']}")