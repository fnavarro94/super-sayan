
#must use python2
import sys
import uproot, uproot_methods
import numpy as np
sys.path.append('/home/felipe/super_sayan/super-sayan/super_saiyan/helpers')
import JetReCalibrator_saiyan
from JetReCalibrator_saiyan import *
from awkward import JaggedArray, Table


JRC = JetReCalibratorSaiyan("Jec10V","AK5PF",True,"/home/felipe/super_sayan/super-sayan/super_saiyan/helpers/data",calculateType1METCorrection=True,calculateSeparateCorrections=True)

  


columns = ['Electron_pt']


for arrays in uproot.tree.iterate('root_files/nano.root','Events',columns,entrysteps=5000):
     
    e = arrays['Electron_pt']
    print arrays['Electron_pt'][100:103]
	

 

