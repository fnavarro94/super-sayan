class VHTreeProducer(Module):

    def __init__(self, channel, **kwargs):
        self._channel = channel  # '0L', '1L', '2L'
        self._systOpt = {'jec':False, 'jes':None, 'jes_source':'', 'jer':'nominal', 'jmr':None, 'met_unclustered':None}
        for k in kwargs:
            self._systOpt[k] = kwargs[k]

        logging.info('Running %s channel with systematics %s', self._channel, str(self._systOpt))
        
        self.jetmetCorr = JetMETCorrector(jetType="AK4PFchs",
                                          jec=self._systOpt['jec'],
                                          jes=self._systOpt['jes'],
                                          jes_source=self._systOpt['jes_source'],
                                          jer=self._systOpt['jer'],
                                          met_unclustered=self._systOpt['met_unclustered'])
        self.subjetCorr = JetMETCorrector(jetType="AK4PFPuppi",
                                          jec=self._systOpt['jec'],
                                          jes=self._systOpt['jes'],
                                          jes_source=self._systOpt['jes_source'],
                                          jer=self._systOpt['jer'],
                                          jmr=self._systOpt['jmr'],
                                          met_unclustered=self._systOpt['met_unclustered'])

    def _correctJetAndMET(self, event):
        event._allJets = Collection(event, "Jet")
        event.ak15Subjets = Collection(event, "AK15PuppiSubJet")  # do not sort after updating!!
        event.met = METObject(event, "MET")

        if self.isMC or self._systOpt['jec']:
            rho = event.fixedGridRhoFastjetAll
            # correct AK4 jets and MET
            self.jetmetCorr.setSeed(rndSeed(event, event._allJets))
            self.jetmetCorr.correctJetAndMET(jets=event._allJets, met=event.met, rho=rho,
                                             genjets=Collection(event, 'GenJet') if self.isMC else None,
                                             isMC=self.isMC, runNumber=event.run)
            event._allJets = sorted(event._allJets, key=lambda x : x.pt, reverse=True)  # sort by pt after updating
            # correct AK15 subjets
            self.subjetCorr.setSeed(rndSeed(event, event.ak15Subjets))
            self.subjetCorr.correctJetAndMET(jets=event.ak15Subjets, met=None, rho=rho,
                                             genjets=Collection(event, 'GenSubJetAK15') if self.isMC else None,
                                             isMC=self.isMC, runNumber=event.run)

        # construct AK15 p4 from (updated) subjets
        event._allAK15jets = Collection(event, "AK15Puppi")
        for fj in event._allAK15jets:
            fj.subjets = get_subjets(fj, event.ak15Subjets, ('subJetIdx1', 'subJetIdx2'))
            newP4 = ROOT.TLorentzVector()
            if len(fj.subjets) == 2:
                newP4 = fj.subjets[0].p4() + fj.subjets[1].p4()
            fj.pt, fj.eta, fj.phi, fj.mass, fj.msoftdrop = newP4.Pt(), newP4.Eta(), newP4.Phi(), newP4.M(), newP4.M()

        # jet mass resolution smearing
        if self.isMC and self._systOpt['jmr']:
            self.subjetCorr.setSeed(rndSeed(event, event.ak15Subjets, 1))
            self.subjetCorr.smearJetMass(jets=event._allAK15jets, gensubjets=Collection(event, 'GenSubJetAK15'), isMC=True)

        event._allAK15jets = sorted(event._allAK15jets, key=lambda x : x.pt, reverse=True)  # sort by pt
