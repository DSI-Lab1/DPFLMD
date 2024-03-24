import numpy as np

def sampleClients(args,orig_traj_num):
    m = args.num_participants
    clients = []
    for i in range(args.duplicate):
        clients.extend(list(range(orig_traj_num)))
    if m <= len(clients):
        res = np.random.choice(clients,m,replace=False)
    else:
        # Select the same client multiple times
        res = np.random.choice(clients,m,replace=True)
    return res