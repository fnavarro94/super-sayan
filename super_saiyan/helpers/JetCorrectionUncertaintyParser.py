import uproot, uproot_methods
import numpy as np
import ntpath
from numpy import sqrt,log,exp,abs
from numpy import maximum as max
from numpy import minimum as min
from numpy import power as pow

filePath = "files/residual.txt"
f = open(filePath, 'r').readlines()
'''
This script parses a Jet correction txt file and stores its components in arrays.
It creates the following variables:

1) binParameters     list with the names of the variables that are expected to perform the lookup
2) functionParameters    list with the names of the variables that are expected to evaluate the function
3) bins              list with the binnig of the binParameters  * currently only for 1D, one binParameter
4) funcParamLimits_vec    a vector containing dictionaries each with the the upper an lower limits of the function parameters 
5) tableFuncParams        a vector containing the table function parameters 


'''

class UncertaintyParser(object):
	
	def __init__ (self, file_path):
		f = open(filePath, 'r').readlines()
		bins = [] #contains bin values
		binsTemp = [] # used to build bins variable
		binParameters = [] # names of the expected parameters used for bin lookup
		functionParameters = [] # names of the expected parameters required to evaluate the function
		#tableFunctionParameters = [] # names of the table function parameters as they will be named in the function (p1,p2,p3)
		possibleCorrections = ['L1FastJet','L2Relative','L3Absolute']
		
		params_raw = f[0].strip().strip('{').strip('}').split()
		params_raw[0].strip('{')
		params_raw[len(params_raw)-1].strip('}')
		params = params_raw

		num_binParams = int(params[0])
		num_funcParams = int(params[num_binParams + 1])
		num_allParams = num_binParams + num_funcParams
		#num_tableFuncParams = int(f[1].split()[num_binParams*2])-num_funcParams*2
		function = params[2+num_funcParams+num_binParams]
		#for i in range(num_tableFuncParams):
		#	tableFunctionParameters.append("p%i"%i)
		for n in range(1,num_binParams + 1):
			binParameters.append(params[n])
		for n in range(num_binParams +2,num_binParams+num_funcParams+2):
			functionParameters.append(params[n])
		allParams = functionParameters
		nParms      = 0
		secondBins_vec = []
		secondBinsNorm_vec = []
		uncertainty_plus = []
		uncertainty_minus = []
		for n, line in enumerate(f):
			secondBins_temp = []
			un_p = []
			un_m = []
			if n==0 or line=='\n':
				continue
			else:
				vecLine = line.split()
				bins.append(float(vecLine[0]))
				binsTemp.append(float(vecLine[1]))
				
				num_second_bins = int(int(vecLine[2*num_binParams])/3)
				
				for i in range(num_second_bins):
					secondBins_temp.append(float(vecLine[2*num_binParams+i*3 +1]))
					un_p.append(float(vecLine[i*3+4]))
					un_m.append(float(vecLine[i*3+5]))
		    
			secondBinsNorm_temp = (np.array(secondBins_temp) - secondBins_temp[0])/(secondBins_temp[len(secondBins_temp)-1]) + n-1
			secondBinsNorm_vec.append(secondBinsNorm_temp)
			secondBins_vec.append(secondBins_temp)
			uncertainty_plus.append(un_p)
			uncertainty_minus.append(un_m)
		bins.append(binsTemp[len(binsTemp)-1])
		
		
		self.secondBins = np.array(secondBins_vec)
		self.secondBinsNorm = np.array(secondBinsNorm_vec)
		self.uncertaintyP = np.array(uncertainty_plus).flatten()
		self.uncertaintyM = np.array(uncertainty_minus).flatten()
		self.nBinParams = num_binParams
		self.nFuncParams = num_funcParams
		self.binParams  = binParameters   
		self.funcParams = functionParameters
		self.bins           = np.array(bins)        
		self.allParams = allParams
		
	
	def evalFirstIndex(self, param1):
		print(param1)
		evalParam1_temp = np.maximum(param1,self.bins[0])
		print(evalParam1_temp)
		evalParam1 = np.minimum(evalParam1_temp,self.bins[len(self.bins)-1]-0.1)
		print(evalParam1)
		bins = self.bins
		index = np.searchsorted(bins,evalParam1, side='right')-1
		
		
		return index
		
	def evalSecondIndex(self, binParam1,binParam2):
		bin1  = self.evalFirstIndex(binParam1)
		bin2 = self.secondBinsNorm.flatten()
		func = lambda min_,max_,bin1_,param2: bin1_ +(param2-min_)/(max_)
		minBin = self.secondBins[bin1][:,0]
		maxBin = self.secondBins[bin1][:,len(self.secondBins)-1]
		
		binParamNorm = func(minBin,maxBin,bin1,binParam2)
		secondIndex = np.maximum(secondIndex,bin1)
		secondIndex = np.minimum(secondIndex,bin1+0.999)
		secondIndex = np.searchsorted(bin2,binParamNorm, side='right')-1
		
		return secondIndex
	
		
	def evalUncertainty(self, param1, param2):
		
		
		
		index1 = self.evalFirstIndex(param1)
		index2 = self.evalSecondIndex(param1, param2)
		
		uncert = self.uncertaintyP[index2]
		
		return uncert
		
			
		
	
