
#must use python2

import uproot, uproot_methods
import numpy as np
from awkward import JaggedArray, Table
   

  


columns = ['Electron_pt']


for arrays in uproot.tree.iterate('root_files/nano.root','Events',columns,entrysteps=5000):
     
    e = arrays['Electron_pt']
    print arrays['Electron_pt']	
	

 

