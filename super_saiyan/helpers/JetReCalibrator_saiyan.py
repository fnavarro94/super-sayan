import numpy as np
import awkward
import sys
import uproot, uproot_methods
sys.path.append("/home/felipe/saiyan/saiyan/saiyan/arrays")
import Builder  # (saiyan tools)
from JetCorrectionParser import CorrectionParser




class JetRecalibrator_saiyan:
    def __init__(self,globalTag,jetFlavour,doResidualJECs,jecPath,upToLevel=3,calculateSeparateCorrections=False,calculateType1METCorrection=False, type1METParams={'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True} ):
        self.globalTag = globalTag
        self.jetFlavour = jetFlavour
        self.doResidualJECs = doResidualJECs
        self.jecPath = jecPath
        self.upToLevel = upToLevel
        self.calculateType1METCorr = calculateType1METCorrection
        self.type1METParams  = type1METParams
        # Make base corrections
        #path = os.path.expandvars(jecPath) #"%s/src/CMGTools/RootTools/data/jec" % os.environ['CMSSW_BASE'];
        path = self.jecPath
        self.L1JetPar  = CorrectionParser("%s/%s_L1FastJet_%s.txt" % (path,globalTag,jetFlavour),"");
        self.L2JetPar  = CorrectionParser("%s/%s_L2Relative_%s.txt" % (path,globalTag,jetFlavour),"");
        self.L3JetPar  = CorrectionParser("%s/%s_L3Absolute_%s.txt" % (path,globalTag,jetFlavour),"");
        self.vPar = [self.L1JetPar]
        
        if upToLevel >= 2: self.vPar.append(self.L2JetPar);
        if upToLevel >= 3: self.vPar.append(self.L3JetPar);
        # Add residuals if needed
        if doResidualJECs : 
            self.ResJetPar = CorrectionParser("%s/%s_L2L3Residual_%s.txt" % (path,globalTag,jetFlavour))
            self.vPar.append(self.ResJetPar);
        #Step3 (Construct a FactorizedJetCorrector object) 
        #self.JetCorrector = ROOT.FactorizedJetCorrector(self.vPar)
        if os.path.exists("%s/%s_Uncertainty_%s.txt" % (path,globalTag,jetFlavour)):
            self.JetUncertainty = UncertaintyParser("%s/%s_Uncertainty_%s.txt" % (path,globalTag,jetFlavour));
        elif os.path.exists("%s/Uncertainty_FAKE.txt" % path):
            self.JetUncertainty = UncertaintyParser("%s/Uncertainty_FAKE.txt" % path);
        else:
            print 'Missing JEC uncertainty file "%s/%s_Uncertainty_%s.txt", so jet energy uncertainties will not be available' % (path,globalTag,jetFlavour)
            self.JetUncertainty = None
        self.separateJetCorrectors = {}
        #if calculateSeparateCorrections or calculateType1METCorrection:
        #    self.vParL1 = ROOT.vector(ROOT.JetCorrectorParameters)()
        #    self.vParL1.push_back(self.L1JetPar)
        #    self.separateJetCorrectors["L1"] = ROOT.FactorizedJetCorrector(self.vParL1)
        #    if upToLevel >= 2 and calculateSeparateCorrections:
        #        self.vParL2 = ROOT.vector(ROOT.JetCorrectorParameters)()
        #        for i in [self.L1JetPar,self.L2JetPar]: self.vParL2.push_back(i)
        #        self.separateJetCorrectors["L1L2"] = ROOT.FactorizedJetCorrector(self.vParL2)
        #    if upToLevel >= 3 and calculateSeparateCorrections:
        #        self.vParL3 = ROOT.vector(ROOT.JetCorrectorParameters)()
        #        for i in [self.L1JetPar,self.L2JetPar,self.L3JetPar]: self.vParL3.push_back(i)
        #        self.separateJetCorrectors["L1L2L3"] = ROOT.FactorizedJetCorrector(self.vParL3)
        #    if doResidualJECs and calculateSeparateCorrections:
        #        self.vParL3Res = ROOT.vector(ROOT.JetCorrectorParameters)()
        #        for i in [self.L1JetPar,self.L2JetPar,self.L3JetPar,self.ResJetPar]: self.vParL3Res.push_back(i)
        #        self.separateJetCorrectors["L1L2L3Res"] = ROOT.FactorizedJetCorrector(self.vParL3Res)
