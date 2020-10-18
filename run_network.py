from bmtk.simulator import bionet
from matplotlib import pyplot as plt
import pdb
from bmtk.simulator.bionet.pyfunction_cache import add_cell_processor
from bmtk.simulator.bionet.default_setters.cell_models import set_params_peri
from neuron import h
#from bmtk.simulator.bionet.default_setters.cell_models import loadHOC

# Load hoc cell templates
#bionet.pyfunction_cache.add_cell_model(loadHOC, directive='hoc', model_type='biophysical')

def fix(hobj):
    """Replace reconstructed axon with a stub

    :param hobj: hoc object
    """

    h.execute('create axon[2]', hobj)

    for sec in hobj.axon:
        sec.L = 30
        sec.diam = 1
        hobj.axonal.append(sec=sec)
        hobj.all.append(sec=sec)  # need to remove this comment

    hobj.axon[0].connect(hobj.soma[0], 0.5, 0)
    hobj.axon[1].connect(hobj.axon[0], 1, 0)

    h.define_shape()

def my_processor(hobj, cell, dynamics_params):
    if dynamics_params is not None:
        fix(hobj)
        set_params_peri(hobj, dynamics_params)

    return hobj

add_cell_processor(my_processor, overwrite=False)

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
