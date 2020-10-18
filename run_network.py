from bmtk.simulator import bionet
from matplotlib import pyplot as plt
import pdb
#from bmtk.simulator.bionet.default_setters.cell_models import loadHOC

# Load hoc cell templates
#bionet.pyfunction_cache.add_cell_model(loadHOC, directive='hoc', model_type='biophysical')

conf = bionet.Config.from_json('model_info/simulation_config.json')
conf.build_env()
net = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=net)
#import pdb; pdb.set_trace()
sim.run()


#pdb.set_trace()

#plt.plot(sim._seclamps[0]._recorder.as_numpy())
#plt.show()
#stims_chn = sim._iclamps[1].recorder.as_numpy()
#stims_p = sim._iclamps[0].recorder.as_numpy()
#iclamps = sim._iclamps
#pdb.set_trace()
#print(len(sim._iclamps[1].recorder.as_numpy()))
