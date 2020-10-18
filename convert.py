from sumatra.parameters import build_parameters
import json
from hoc2swc import hoc2swc

hoc2swc("OriginalCells/86_L5_CDK20041214_nr3L5B_dend_PC_neuron_transform_registered_C2center_scaled_diameters.hoc",
            "model_info/components/morphologies/86_L5_CDK20041214_nr3L5B_dend_PC_neuron_transform_registered_C2center_scaled_diameters.swc", 
            no_mod=True)
import pdb; pdb.set_trace()
params_all = build_parameters("OriginalCells/86_CDK_20041214_BAC_run5_soma_Hay2013_C2center_apic_rec_scaled_diameters.param")

params = params_all['neuron']

#Variable names to exclude when converting.
exclude = ["spatial", "begin", "end", "outsidescale", "distance", "offset", "linScale", "_lambda", "xOffset"]

type_dic = {'Soma' : "soma", "Dendrite" : "dend", "ApicalDendrite" : "apic", "AIS" : "axon", "Myelin" : "myelin"}


#Takes a section (Soma, Dendrites, etc.) and returns the mechanism conductances in the appropriate .json formats.
def convert_section(params, sec_name):
    params = params['mechanisms']['range']
    results = []
    #import pdb; pdb.set_trace()
    for mech in params.keys():
        if mech != "pas":
            results += convert_mech(sec_name, mech, params[mech])

    return results

#Converts params mech into .json mech.
def convert_mech(sec_name, mech, innards):
    sec = type_dic[sec_name]

    res = []
    if mech != "pas":
        for var in innards.keys():
            
            if var not in exclude:
                val_dic = {}
                val_dic['section'] = sec
                val_dic['name'] = (var + "_" + mech)
                val_dic['value'] = innards[var]
                val_dic['mechanism'] = mech

                res.append(val_dic)

    return res

#Looks through the params and creates the passive section.
def convert_passives(params):
    params = params["neuron"]

    results = {"ra" : {}, "cm" : {}, "g_pas" : {}, "e_pas" : {}}

    for section in params.keys():
        if section != "filename":
            results["ra"][type_dic[section]] = params[section]['properties']["Ra"]
            results["cm"][type_dic[section]] = params[section]['properties']["cm"]

            results["g_pas"][type_dic[section]] = params[section]["mechanisms"]["range"]["pas"]["g"]
            results["e_pas"][type_dic[section]] = params[section]["mechanisms"]["range"]["pas"]["e"]

    for var in results.keys():
        vals = list(results[var].values())
        if all(val == vals[0] for val in vals):
            results[var] = vals[0]
        else:
            var_dicts = []
            for sec in results[var].keys():
                var_dicts.append({"section" : sec, var : results[var][sec]})
            results[var] = var_dicts

    return results

#Looks through the params and creates the conditions section.
def convert_conditions(params):
    result = {}
    result["v_init"] = params["sim"]["Vinit"]
    result["celsius"] = params["sim"]["T"]

    erev = []

    cell = params["neuron"]

    for section in cell.keys():
        if section == "filename":
            continue
        properties = cell[section]["properties"]

        if "ions" in properties.keys():
            props = {"section" : type_dic[section]}
            for prop in properties["ions"]:
                props[prop] = properties["ions"][prop]

            erev.append(props)

    result["erev"] = erev
    return result

passives = convert_passives(params_all)

conditions = convert_conditions(params_all)

#Makes a list of all the mechanism parameters.
genome = []
for sec in params.keys():
    if sec != "filename":
        sec_params = convert_section(params[sec], sec)
        genome += sec_params

file = {}
file["passive"] = [passives]
file["conditions"] = [conditions]
file["genome"] = genome

with open("model_info/components/biophysical_neuron_models/86_CDK_20041214_BAC_run5_soma_Hay2013_C2center_apic_rec_scaled_diameters.json", "w") as f:
    json.dump(file, f, indent = 2)