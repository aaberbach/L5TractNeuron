from bmtk.builder.networks import NetworkBuilder

net = NetworkBuilder('mcortex')
net.add_nodes(N=1,cell_name='PN',
              potental='exc',
              model_type='biophysical',
              model_processing='fullaxon',
              model_template='ctdb:Biophys1.hoc',
              #morphology="Scnn1a_473845048_m.swc",
              morphology="86_L5_CDK20041214_nr3L5B_dend_PC_neuron_transform_registered_C2center_scaled_diameters.swc",
              #morphology="try.swc",
              dynamics_params="86_CDK_20041214_BAC_run5_soma_Hay2013_C2center_apic_rec_scaled_diameters.json"
              #dynamics_params="472363762_fit.json"
              )

# net.add_nodes(N=1,cell_name='Chn',
#               potental='exc',
#               model_type='biophysical',
#               model_template='hoc:chandelierWB',
#               morphology=None
#               )

# conn = net.add_edges(source=net.nodes(cell_name='Chn'), target=net.nodes(cell_name='PN'),
#                    connection_rule=1,
#                    syn_weight=0.01,
#                    #weight_function=None,
#                    target_sections=['axonal'],
#                    #delay=0.0,
#                    distance_range=[0.0, 300.0],
#                    #dynamics_params='GABA_InhToExc.json',
#                    #model_template='Exp2Syn',
#                    is_gap_junction=True)

# conn = net.add_gap_junctions(source=net.nodes(cell_name='Chn'), target=net.nodes(cell_name='PN'),
#                     resistance = 0.01, target_sections=['axonal'])

net.build()
net.save_nodes(output_dir='model_info/network')
# net.save_edges(output_dir='network')

# for node in net.nodes():
#     print(node)

# for edge in net.edges():
#     print(edge)
    
from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(base_dir='model_info',      # Where to save the scripts and config files 
                 components_dir='components',
                 network_dir='model_info/network',    # Location of directory containing network files
                 tstop=10000.0, dt=0.1,     # Run a simulation for 2000 ms at 0.1 ms intervals
                 report_vars=['v'],
                 #clamp_reports=["se"], # Tells simulator we want to record membrane potential and calcium traces
                 current_clamp={           # Creates a step current from 500.ms to 1500.0 ms  
                     'amp': [0.0005],
                     #'std': [0.0, 0.0],
                     'delay': [200],
                     'duration': [10000],
                     'gids':[0]
                 },
                #  file_current_clamp={
                #      "input_file": "PN_IClamp/inputs/amps.h5"
                #  },
                #  se_voltage_clamp={
                #      "amps":[[-70, -70, -70], [-70, -70, -70]],
                #      "durations": [[2000, 2000, 2000], [2000, 2000, 2000]],
                #      'gids': [0, 1],
                #      'rs': [0.001, 0.01],
                #      'name':"PN_se_clamp"
                #  },
                 compile_mechanisms=True   # Will try to compile NEURON mechanisms
                )
                
