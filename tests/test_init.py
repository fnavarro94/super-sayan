import uproot, uproot_methods
from Builder import Initialize

file = uproot.open("nano_5.root")
tree = file["Events"]

e = Initialize({'pt':tree.array("Electron_pt"),
                'eta':tree.array("Electron_eta"),
                'phi':tree.array("Electron_phi"),
                'mass':tree.array("Electron_mass"),
                'iso':tree.array('Electron_pfRelIso03_all'),
                'dxy':tree.array('Electron_dxy'),
                'dz':tree.array('Electron_dz'),
                'id':tree.array('Electron_mvaSpring16GP_WP90')})

mu = Initialize({'pt':tree.array("Muon_pt"),
                 'eta':tree.array("Muon_eta"),
                 'phi':tree.array("Muon_phi"),
                 'mass':tree.array("Muon_mass"),
                 'iso':tree.array('Muon_pfRelIso04_all'),
                 'dxy':tree.array('Muon_dxy'),
                 'dz':tree.array('Muon_dz')})

tau = Initialize({'pt':tree.array('Tau_pt'),
                  'eta':tree.array('Tau_eta'),
                  'phi':tree.array('Tau_phi'),
                  'mass':tree.array('Tau_mass'),
                  'decayMode':tree.array('Tau_idDecayMode'),
                  'decayModeNew':tree.array('Tau_idDecayModeNewDMs'),
                  'id':tree.array('Tau_idMVAnew')})

pho = Initialize({'pt':tree.array('Photon_pt'),
                 'eta':tree.array('Photon_eta'),
                 'phi':tree.array('Photon_phi'),
                 'mass':tree.array('Photon_mass')})

j = Initialize({'pt':tree.array('Jet_pt'),
                'eta':tree.array('Jet_eta'),
                'phi':tree.array('Jet_phi'),
                'mass':tree.array('Jet_mass'),
                'id':tree.array('Jet_jetId')})

fj = Initialize({'pt':tree.array('AK15Puppi_pt'),
                 'eta':tree.array('AK15Puppi_eta'),
                 'phi':tree.array('AK15Puppi_phi'),
                 'mass':tree.array('AK15Puppi_mass'),
                 'jetId':tree.array('AK15Puppi_jetId')})

met = Initialize({'pt':tree.array("MET_pt"),
                  'eta':0,
                  'phi':tree.array("MET_phi"),
                  'mass':0})
'''
gen = Initialize({'pt':tree.array('GenPart_pt'),
                  'eta':tree.array('GenPart_eta'),
                  'phi':tree.array('GenPart_phi'),
                  'mass':tree.array('GenPart_mass'),
                  'pdgid':tree.array('GenPart_pdgId'),
                  'status':tree.array('GenPart_status')})
'''

#print((e.counts)&~(e.pt<7))
diele = e[e.counts>1,0]+e[e.counts>1,1]
print(diele.pt)
#print(pe.delta_r(pmu))
#print(p4.__class__)
#print(met.delta_phi(mu))
#print(e.cross(e, nested=True).i0.delta_r(e.cross(e, nested=True).i1))
#print(e.cross(e, nested=True).i0.iso)
#print(met.__class__)
#print(e['iso'])
#print(e.pt)
#print(met.delta_phi(met.closest(e)))
#print(e.match(e, 0.4))
