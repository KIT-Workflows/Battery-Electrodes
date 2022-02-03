from ase.io.vasp import read_vasp_out
import yaml

def find_line(filename, lookup, pos_vas):

    with open(filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                t_num = num
                var_stg = line.split()[pos_vas]
    #print('found at line:', var_1, t_num)
    #print(var_stg)
    return var_stg

def find_by_key(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif key == target:
            yield value

def call_find_by_key(data, target):

    y = []
    x = None
    
    for x in find_by_key(data, target):
        y.append(x) 
    
    return x

if __name__ == '__main__':

    with open('rendered_wano.yml') as file:
        wano_file = yaml.full_load(file)

    properties_bool = wano_file["TABS"]["Properties"]["properties"]
    import_inputs = wano_file["TABS"]["Properties"]["Import Inputs"]
    
    if properties_bool:
        a_dict = wano_file["TABS"]["Properties"]["Var-properties"]
        var_prop = wano_file["TABS"]["Properties"]["Var-properties"]
        a_key = list(a_dict[0].keys())[0]
        values_of_key = [a_dict[a_key] for a_dict in a_dict]
        
        file_outfile = 'OUTCAR'
        atoms = read_vasp_out(file_outfile)
        results_dict= {}

        #find_line(file_outfile, "NKPTS =", 3)
        results_dict["NKPTS"] = int(find_line(file_outfile, "NKPTS =", 3))
        results_dict["ENCUT"] = wano_file["TABS"]["INCAR"]["ENCUT"]

        for var in values_of_key:
            if var[0].isupper():
                cmd_1 = call_find_by_key(wano_file, var) #wano_file["TABS"]["INCAR"][var]
                results_dict[var] = cmd_1
            else:
                if var == "cell_lengths_and_angles":
                    cmd_1 = "atoms.get_" + var + "()"
                    results_dict['a'] = float(eval(cmd_1)[0])
                    results_dict['c'] = float(eval(cmd_1)[2])
                    print(eval(cmd_1)[0],eval(cmd_1)[2])
                else:
                    cmd_1 = "atoms.get_" + var + "()"
                    results_dict[var] = eval(cmd_1)
    else:
        results_dict = {}
    
    if import_inputs:
        with open('Inputs.yml') as file:
            input_file = yaml.full_load(file)
        results_dict.update(input_file)

    with open("dft_vasp_dict.yml",'w') as out:
        yaml.dump(results_dict, out,default_flow_style=False)
    
    with open("output_dict.yml",'w') as out:
        yaml.dump(results_dict, out,default_flow_style=False)
    