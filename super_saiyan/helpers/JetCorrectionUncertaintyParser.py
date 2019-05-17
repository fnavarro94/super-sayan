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
		    
			secondBinsNorm_temp = (np.array(secondBins_temp) - secondBins_temp[0])/(secondBins_temp[len(secondBins_temp)-1]) + n
			secondBinsNorm_vec.append(secondBinsNorm_temp)
			secondBins_vec.append(secondBins_temp)
			uncertainty_plus.append(un_p)
			uncertainty_minus.append(un_m)
		bins.append(binsTemp[len(binsTemp)-1])
		
		
		self.secondBins = np.array(secondBins_vec)
		self.secondBinsNorm = np.array(secondBinsNorm_vec)
		self.uncertaintyP = uncertainty_plus
		self.uncertaintyM = uncertainty_minus
		self.nBinParams = num_binParams
		self.nFuncParams = num_funcParams
		self.binParams  = binParameters   
		self.funcParams = functionParameters
		self.bins           = np.array(bins)        
		self.allParams = allParams
		
	
	def evalFirstIndex(self, binParam):
		
		bins = self.bins
		index = np.searchsorted(bins,binParam, side='right')-1
		for i in range(len(index)):
			continue
		
		return index
		
	def evalSecondIndex(self, binParam1,binParam2):
		bin1  = self.evalFirstIndex(binParam1)
		func = lambda min_,max_,bin1,param2: bin1 +(param2-min_)/(max_)
	
	
		
	def evalUncertainty(self, *parameters):
		index = self.evalIndex(parameters[0])
		evalVars = []
		for n, var in enumerate(parameters):
			if n != 0:
				# clamping the function paramterer values to the minimums and maximums defined in correction txt file
				evalVars_temp = np.maximum(np.array(parameters[n]),self.funcParamLimits[self.funcParams[n-1]][0][index])
				evalVars.append(np.minimum(evalVars_temp,self.funcParamLimits[self.funcParams[n-1]][1][index]))
				self.a =  np.array(parameters[n])
				self.b=self.funcParamLimits[self.funcParams[n-1]][0][index]
					
		for n, var in enumerate(self.tableFuncParams):
			evalVars.append(self.tableFuncParamValues[self.tableFuncParams[n]][index])
			
		self.vars=evalVars
		
		result = self.function(*tuple(evalVars))
		return result
			
		
	
