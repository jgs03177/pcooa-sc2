import json
import os
import errno
import torch


# process [{'Quantity': a1, 'UnitTypeID': b1}, ...] to {b1:a1, ....}
def tuplelist_to_dict(tuplelist):
    p_dict = dict()
    if tuplelist is not None:
        for e in tuplelist:
            p_dict[e["UnitTypeID"]] = e["Quantity"]
    return p_dict


# gets input data of the array
def extract_battledict(battledict):
    #print(battledict)
    items = battledict.setdefault("items", dict())
    squad1 = battledict["combination"].setdefault("squad_p1", dict())
    squad2 = battledict["combination"].setdefault("squad_p2", dict())
    p_squad1 = tuplelist_to_dict(squad1)
    p_squad2 = tuplelist_to_dict(squad2)
    for i in items:
        i["squad_p1"] = tuplelist_to_dict(i["squad_p1"])
        i["squad_p2"] = tuplelist_to_dict(i["squad_p2"])
    return items, p_squad1, p_squad2


def extract_battlelogs_pickle(foldername, picklename=None):
    # generate folder
    if not os.path.exists("./pickles"):
        try:
            os.makedirs("./pickles")
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise

    # get pickle if exists
    if picklename is not None:
        picklename = os.path.join("./pickles/", picklename)
    if picklename is not None and os.path.isfile(picklename):
        pickle = torch.load(picklename)
        l_item = pickle.setdefault("l_item", list())
        l_squad1 = pickle.setdefault("l_squad1", list())
        l_squad2 = pickle.setdefault("l_squad2", list())
        l_unmapper = pickle.setdefault("l_unmapper", list())
        
    # if not, get from txt file and make pickle
    else:
        l_item, l_squad1, l_squad2, l_unmapper = extract_battlelogs(foldername)

        # generate pickle
        if picklename is not None:
            pickle = dict()
            pickle["l_item"] = l_item
            pickle["l_squad1"] = l_squad1
            pickle["l_squad2"] = l_squad2
            pickle["l_unmapper"] = l_unmapper
            torch.save(pickle, picklename)

    return l_item, l_squad1, l_squad2, l_unmapper


# 
def enlist_logfiles(foldername, exts=None):
    files = os.listdir(foldername)
    output = []
    for filename in files:
        # consider only .json
        name, ext = os.path.splitext(filename)
        if exts is not None and ext not in exts:
            continue
        fullfilename = os.path.join(foldername, filename)
        output.append(fullfilename)
    return output


# 
def extract_battlelogs(foldername):
    l_item = list()
    l_squad1 = list()
    l_squad2 = list()
    s_unittypeid = set()

    # read all jsons in the folder
    json_list = enlist_logfiles(foldername, [".json"])
    for json_fullpath in json_list:
        with open(json_fullpath) as battlejsonfile:
            battledict = json.load(battlejsonfile)
            o = extract_battledict(battledict)
            item, squad1, squad2 = o
            l_item.append(item)
            l_squad1.append(squad1)
            l_squad2.append(squad2)
            s_unittypeid.update(squad1.keys())
            s_unittypeid.update(squad2.keys())
            # s_unittypeid.update(remaining.keys())

    l_unmapper = list(s_unittypeid)
    l_unmapper.sort()

    return l_item, l_squad1, l_squad2, l_unmapper


# test
if __name__ == '__main__':
    #f = json.load(open(r"E:\output\BushOne\mp\r_1.json"))
    #a = extract_battledict(f)
    #print(a)
    b = extract_battlelogs(r"E:\output\BushOne\mp")
    for e in b:
        print(e)