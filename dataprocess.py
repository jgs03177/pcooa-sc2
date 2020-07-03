import pandas as pd
import numpy as np


def ulist2mapper(ulist):
    mapper = dict()
    for y, x in enumerate(ulist, 0):
        mapper[x] = y
    return mapper

def squad_dict2list(squad_dict, base_ulist):
    mapper = ulist2mapper(base_ulist)
    squad_list = np.zeros(len(base_ulist))
    for key, value in squad_dict.items():
        squad_list[mapper[key]] = value
    return squad_list

def split_table_for_cv(table, nblocks):
    ndatalen = len(table)
    # do not use df.loc, this includes both endpoints.
    tablelet = [table[(i*ndatalen)//nblocks:((i+1)*ndatalen)//nblocks] for i in range(nblocks)]
    return tablelet
    
def get_cv_datatable(tablelet, i):
    testtable = tablelet[i]
    traintable = pd.concat(tablelet[:i] + tablelet[i+1:], axis=0)
    return traintable, testtable

# process values (array of squaddict) to ndarray
def squad_dict2list_batch(values, base_ulist):
    return np.array(list(map(lambda x: squad_dict2list(x, base_ulist), values)))

def test_dataprocess():
    p_unit_columns = [4, 73, 74, 75, 76, 77, 83, 141, 311]
    z_unit_columns = [9, 105, 107, 109, 110, 126, 688]
    pz_unit_columns = [4, 9, 73, 74, 75, 76, 77, 83, 105, 107, 109, 110, 126, 141, 311, 688]
    #unit_columns = [4, 9, 32, 33, 34, 35, 48, 49, 50, 51, 52, 53, 73, 74, 75, 76, 77, 83, 105, 107, 109, 110, 126, 141, 311, 484, 688, 691, 692]
    p_mapper = ulist2mapper(p_unit_columns)
    print(p_mapper)
    
    maps = ["Plain"]
    #["mp","pp", "mz", "zz", "zp"]
    unittypes = ["pp", "zz", "zp"]
    columns = [(p_unit_columns, p_unit_columns), (z_unit_columns, z_unit_columns), (z_unit_columns, p_unit_columns)]
    oo = make_table_macro(r"E:/output0421/output", maps, unittypes, pickleprefix="output0421_")
    print(oo[2])
    table_idx = 2
    table = oo[table_idx]
    column_index_p1, column_index_p2 = columns[table_idx]
    # 1
    traintable, testtable = table[:500], table[500:]
    # 2
    #nblocks = 10
    #tablelet = split_table_for_cv(table, nblocks)
    #print(tablelet[0][("setup", "squad_p1")].values)
    #traintable, testtable = get_cv_dataset(tablelet, 9)
    #print(trainset)

if __name__=="__main__":
    test_datasplit()