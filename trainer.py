import torch
import torch.nn as nn
import torch.nn.functional as F


verbose = True

def print_wrapped(*args):
    if verbose:
        print(*args)

def train_1epoch(dl, net, criterion, optimizer):
    net.train()
    batch_loss = []
    for i, data in enumerate(dl):
        x1, y1 = data
        optimizer.zero_grad()
        y1hat = net(x1).squeeze()
        loss = criterion(y1hat, y1)
        loss.backward()
        optimizer.step()
        print_wrapped("loss: %.7f" % loss.item())
        batch_loss.append(loss.item())
    return sum(batch_loss)/len(batch_loss)

def test_1epoch(dl, net, criterion):
    net.eval()
    batch_loss = []
    with torch.no_grad():
        for i, data in enumerate(dl):
            x1, y1 = data
            y1hat = net(x1).squeeze()
            loss = criterion(y1hat, y1)
            print_wrapped("loss: %.7f" % loss.item())
            batch_loss.append(loss.item())
    net.train()
    return sum(batch_loss)/len(batch_loss)


def test_1epoch_2args(dl, net, criterion):
    net.eval()
    batch_loss_1, batch_loss_2 = [], []
    with torch.no_grad():
        for i, data in enumerate(dl):
            x1, y1 = data
            y1hat = net(x1).squeeze()
            loss_1, loss_2 = criterion(y1hat, y1)
            print_wrapped("loss: %.7f" % loss_1.item(), loss_2.item())
            batch_loss_1.append(loss_1.item())
            batch_loss_2.append(loss_2.item())
    net.train()
    return sum(batch_loss_1)/sum(batch_loss_2)


def count_correct_predictions_2args(y1hat, y1):
    # evaluation
    y1hatp = y1hat >= 0.0001
    y1hatn = y1hat <= -0.0001
    if False:
        y1p = y1 >= 0.9999
        y1n = y1 <= 0.0001
    else:
        y1p = y1 >= 0.5001
        y1n = y1 <= 0.4999

    guess = (y1p & y1hatp) | (y1n & y1hatn)

    correct_guesses = torch.sum(guess)
    total_guesses = torch.sum(y1p) + torch.sum(y1n)

    return correct_guesses.to(torch.float32), total_guesses.to(torch.float32)

def test_trainer():
    import torch.optim as optim
    
    naivenet = NetDNN(len(column_index_p1)+ len(column_index_p2), 32, 32, 32, 32, 1).to(target_device, target_dtype)
    net = naivenet
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    print(net)
    for i in range(200):
        train_1epoch(traindl, net, criterion, optimizer)
    acc1 = test_1epoch_2args(traindl, net, count_correct_predictions_2args)
    acc2 = test_1epoch_2args(testdl, net, count_correct_predictions_2args)
    print("train_acc = {}, test_acc = {}".format(acc1, acc2))