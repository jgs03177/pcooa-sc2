import torch
import torch.nn as nn
import torch.nn.functional as F


class NetDNN(nn.Module):
    """dnn stack of linear + relu
    #stacks = len(args) - 1
    """
    def __init__(self, *args, dropout=0):
        super(NetDNN, self).__init__()
        
        self.nstacks = len(args) - 1
        assert(self.nstacks > 0)
        self.layers = nn.ModuleList([nn.Linear(args[i], args[i+1]) for i in range(self.nstacks)])
        self.dropout = dropout
        
    def forward(self, x):
        y = x
        if self.dropout == 0:
            for i in range(self.nstacks - 1):
                y = self.layers[i](y)
                y = F.relu(y)
            # last layer has no relu
            y = self.layers[-1](y)
        else:
            for i in range(self.nstacks - 1):
                y = self.layers[i](y)
                y = F.dropout(y, p=self.dropout)
                y = F.relu(y)
            # last layer has no relu
            y = self.layers[-1](y)
            y = F.dropout(y, p=self.dropout)
        return y


class ODNet(nn.Module):
    """dnn stack of linear + relu
    #stacks = len(args) - 1
    """
    def __init__(self, ns1, ns2, nfeats, *, dropout=0):
        """
        ns1,ns2 : # of input features.
        nfeats : # of hidden features"""
        super(ODNet, self).__init__()

        self.Wo1 = nn.Linear(ns1, nfeats, bias=False)
        self.Wd1 = nn.Linear(ns1, nfeats, bias=False)
        
        self.Wo2 = self.Wo1
        self.Wd2 = self.Wd1
        #self.Wo2 = nn.Linear(ns2, nfeats, bias=False)
        #self.Wd2 = nn.Linear(ns2, nfeats, bias=False)

        self.ns = ns1, ns2
        
        assert dropout==0, "dropout is not implemented."
        self.dropout = dropout
        
    def forward(self, x):
        x1, x2 = torch.split(x, self.ns, dim=1)
        if self.dropout == 0:
            Wox1 = self.Wo1(x1)
            Wox2 = self.Wo2(x2)
            Wdx1 = self.Wd1(x1)
            Wdx2 = self.Wd2(x2)
            p1 = Wox1 / Wdx2
            p2 = Wox2 / Wdx1
            #print(p1.shape, p2.shape)
            y1 = torch.sum(p1, axis=1)
            y2 = torch.sum(p2, axis=1)
            #print(y1.shape, y2.shape)
            y = y1-y2
        else:
            raise
        return y


class FunctionConcat(nn.Module):
    """Concatenate functions, not in sequential, but in parallel."""
    def __init__(self, fns, input_sections):
        """
        functions: iterable of functions to concatenate. If arg has none, identity function is used.
        input_sections: iterable of size of inputs of nets"""
        super(FunctionConcat, self).__init__()
        
        nfns = len(fns)
        nsections = len(input_sections)
        assert(nfns == nsections)
        self.nsec = nsections
        
        self.fns = nn.ModuleList(fns)
        self.sections = input_sections
        
    def forward(self, x):
        xs = torch.split(x, self.sections, dim=1)
        ys = []
        for i in range(self.nsec):
            x, f = xs[i], self.fns[i]
            y = f(x) if f is not None else x
            ys.append(y)
        y = torch.cat(ys, dim=1)
        return y


def BattleNet(basenet, inputsize, terrainsize, *args, dropout=0):
    return nn.Sequential(
        FunctionConcat([basenet, basenet, None], [inputsize, inputsize, terrainsize]) 
        #if terrainsize != 0 else FunctionConcat([basenet, basenet], [inputsize, inputsize])
        ,
        nn.ReLU(),
        NetDNN(*args, dropout=dropout)
    )