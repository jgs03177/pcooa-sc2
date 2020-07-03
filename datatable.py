import jsonreader
import pandas as pd
import numpy as np
import os


def battle_stat(item):
    distribution = np.zeros(5, dtype=np.int)
    winratedict = dict()
    result = 0
    itemlen = len(item)
    for i in item:
        result_str = i["result"]
        if result_str == "p1_win":
            result += 1
        elif result_str == "p2_win":
            result -= 1
        elif result_str == "draw":
            pass  # result += 0
        elif result_str == "timeout":
            pass  # result += 0
        else:
            pass  # result += 0
    winrate = (result + itemlen) / (itemlen * 2)

    for i in item:
        result_str = i["result"]
        if result_str == "p1_win":
            distribution[0] += 1
        elif result_str == "p2_win":
            distribution[1] += 1
        elif result_str == "draw":
            distribution[2] += 1
        elif result_str == "timeout":
            distribution[3] += 1
        else:
            distribution[4] += 1
    return winrate, distribution

def battle_stats(l_item):
    winratedict = dict()
    total_winrate = list()
    total_distrib = np.zeros(5, dtype=np.int)
    for item in l_item:
        winrate, distribution = battle_stat(item)
        winratedict["{:f}".format(winrate)] = winratedict.get("{:f}".format(winrate), 0) + 1
        total_distrib += distribution
        total_winrate.append(winrate) 
    return total_winrate, total_distrib, winratedict
    
def make_table_items(l_item):
    # process each items as a table
    tlist = [pd.DataFrame(l_item[i]) for i in range(2000)]
    # concatenate all battles
    table = pd.concat(tlist, keys=list(range(2000)))
    # move item index from row to column
    table = table.unstack(1)
    # reindex (x,y,z) = (battle, item, table)
    table.columns = table.columns.reorder_levels([1,0])
    table = table.reindex(columns=table.columns.sort_values())
    return table

def make_table_setup(l_squad1, l_squad2, aug):
    return pd.DataFrame({("setup", "squad_p1"):l_squad1, ("setup", "squad_p2"):l_squad2, ("setup", "battlefield"):aug})

def make_table(path, aug, picklename=None):
    l_item, l_squad1, l_squad2, _ = jsonreader.extract_battlelogs_pickle(path, picklename)
    a = make_table_setup(l_squad1, l_squad2, aug)
    b = make_table_items(l_item)
    
    winrates, statistics, winratedict = battle_stats(l_item)
    w = pd.DataFrame({("statistics", "winrates"):winrates})
    
    return pd.concat([a,w, b], axis=1)
    
def make_table_macro(basepath, terrains, squadgroup, *,pickleprefix=""):
    p1 = basepath 
    lttable = []
    
    for i, e in enumerate(squadgroup):
        for j, t in enumerate(terrains):
            p2 = t
            p3 = e
            p0 = os.path.join(p1,p2,p3)
            aug = j
            ttable = make_table(p0, aug, pickleprefix + "{}_{}.bpk".format(t,e))
            lttable.append(ttable)
    return lttable

def test_datatable():
    l_item, l_squad1, l_squad2, zz = jsonreader.extract_battlelogs(r"E:\output\Plain\zz")
    print(zz)
    print(l_item)
    print(battle_stats(l_item))
    base = ["Plain"]
    bushes = ["BushOne", "BushTwo", "BushSide"]
    corridors = ["Corridor1", "Corridor2", "Corridor3", "Corridor5"]
    plains = ["PlainSlow"] # "PlainFast" is for the latest binary
    ramps = ["Ramp1", "Ramp2", "Ramp3", "Ramp5"]
    symmetric = ["mp", "mz", "pp", "zz", "zp"]
    asymmetric = ["mp", "mz", "pp", "zz", "zp", "ppr", "zzr", "zpr"]
    o = make_table_macro(r"E:/output", base, symmetric)
    print(o[0])
    print(o[0]['setup']['squad_p1'][2])
    
if __name__=="__main__":
    test_table()