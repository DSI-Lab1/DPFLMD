'''
    Calculate ground truth with standard Apriori algorithm
'''
import itertools
from collections import defaultdict
import multiprocess
import math
from models.seqUtils import seqUtils

def ground_truth_worker(dataset, candidates, participents, queue):
    local_support_count = defaultdict(lambda: 0)
    for idx in range(len(participents)):
        client_idx = participents[idx]
        for candi in candidates:
            if candi in dataset[client_idx]:
                local_support_count[candi] += 1

    queue.put(local_support_count)
    return

def FirstGenCan(alphabet,minl):
        init_candidates = []
        can = itertools.product(alphabet, repeat=minl)
        for c in can:
            c = ''.join(c)
            init_candidates.append(c)
        return init_candidates

def generateC(accept,alphabet):
    C = []
    for ac in accept:
        for i in alphabet:
            C.append(ac+i)
    return C

def groundTruth(dataset, args):
    util = seqUtils()
    k = args.k * len(dataset)
    traj_num = len(dataset)
    frag_len = args.minl - 1
    res = {}
    # alphabet =  ["A", "G", "C", "T"]
    alphabet = ["a", "g", "c", "t"]
    # longer fragments
    while True:
        frag_len += 1
        if frag_len == args.maxl+1:
            return res

        if frag_len == args.minl:
            candidates = FirstGenCan(alphabet,args.minl)
        else:
            candidates = generateC(fragments,alphabet)


        if len(candidates) == 0:
            return res

        support_count = defaultdict(lambda: 0)
        if args.process <= 0:
            for traj_idx in range(traj_num):
                traj = dataset.get_trajectory(traj_idx)
                for candi in candidates:
                    if traj.checkSub(candi) is True:
                        support_count[candi] += 1

                if traj_idx % 10000 == 0 and args.verbose:
                    print("%d trajectories checked" % traj_idx)
        else:
            mananger = multiprocess.Manager()
            queue = mananger.Queue()
            jobs = []
            workload = math.floor(traj_num / args.process)
            for proc_idx in range(args.process):
                if proc_idx == args.process - 1:
                    participents_load = list(range(proc_idx * workload, traj_num))
                else:
                    participents_load = list(range(proc_idx * workload, (proc_idx + 1) * workload))
                args.verbose = True
                p = multiprocess.Process(target=ground_truth_worker,
                                         args=(dataset, candidates, participents_load, queue))
                jobs.append(p)
                p.start()

            for p in jobs:
                p.join()

            proc_results = [queue.get() for j in jobs]

            for proc_res in proc_results:
                for key, value in proc_res.items():
                    support_count[key] += value

        fragments = [key for key, value in support_count.items() if value >= k]
        for key, value in support_count.items():
            if value >= k:
                res[key] = value

        #print("%d-fragments: %d admitted" % (frag_len, len(fragments)))
