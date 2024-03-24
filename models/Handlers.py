import abc
from collections import defaultdict
import multiprocess
from models.Sandwich import FfpaServer
import math
from models.Randomize import Randomizer
from utils.Sampling import sampleClients

def gen_pnext(substring):
    index, m = 0, len(substring)
    pnext = [0]*m
    i = 1
    while i < m:
        if (substring[i] == substring[index]):
            pnext[i] = index + 1
            index += 1
            i += 1
        elif (index!=0):
            index = pnext[index-1]
        else:
            pnext[i] = 0
            i += 1
    return pnext

def KMP_algorithm(string, substring):
    pnext = gen_pnext(substring)
    n = len(string)
    m = len(substring)
    i, j = 0, 0
    while (i<n) and (j<m):
        if (string[i]==substring[j]):
            i += 1
            j += 1
        elif (j!=0):
            j = pnext[j-1]
        else:
            i += 1
    if (j == m):
        return i-j
    else:
        return -1

class Handler(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def run(self):
        pass

class flmdHandler(Handler):
    def __init__(self,args,dataset):
        self.args = args
        # self.alphabet =  ["A", "G", "C", "T"]
        self.alphabet = ["a","g","c","t"]
        self.args.eta = self.__calculateEta()
        self.dataset = dataset
        self.orig_rec_num = len(self.dataset)
        self.clients_num = self.orig_rec_num
        self.args.num_clients = self.clients_num
        self.server = FfpaServer(self.args)
        self.randomizer = Randomizer(self.args)
        self.server.FirstGenCan(self.alphabet,self.args.minl)
        self.round = 0

    def run(self):
        while True:
            if self.server.terminal(self.round,self.args.maxl,self.args.minl) is True:
                self.args.round = self.round
                return self.server.accept_pool.pool
            self.round += 1
            participents = sampleClients(self.args, self.orig_rec_num)
            self.args.num_candidate = self.server.candidateNum()

            support_count = defaultdict(lambda: 0)
            for idx in range(len(participents)):
                client_idx = participents[idx]
                Mergecandidates = self.server.drawCandidate()
                res = self.__oneClient(client_idx, Mergecandidates)

                for key, value in res.items():
                    if key not in support_count.keys():
                        support_count[key] = [0, 0]
                    support_count[key][value] += 1

            accept = self.server.uploadSupportCount(support_count)


    def __processWorker(self,proc_idx,participents,queue):
        support_count = defaultdict(lambda : 0)
        for idx in range(len(participents)):
            client_idx = participents[idx]
            Mergecandidates = self.server.drawCandidate()
            res = self.__oneClient(client_idx,Mergecandidates)
            for key,value in res.items():
                if key not in support_count.keys():
                    support_count[key] = [0,0]
                support_count[key][value] += 1

        queue.put(support_count)
        return
    def __oneClient(self,client_idx,Mergecandidates):
        candi_save = []
        for i in Mergecandidates:
            s = i[0:(len(i) - len(self.alphabet))]
            for j in self.alphabet:
                candi_save.append(s+j)

        response = [0] * len(candi_save)
        ynum = 0
        for i in range(len(candi_save)):
            if candi_save[i] in self.dataset[client_idx]:
                response[i] = 1
                ynum = ynum + 1
        response = self.randomizer.randomBits(response)
        final_response = {}
        for i in range(len(candi_save)):
            final_response[candi_save[i]] = response[i]
        return final_response

    def __calculateEta(self):
        epsilon = self.args.epsilon
        candidates = self.args.num_candidate
        return 1/(1 + math.pow(math.e,(epsilon/candidates)))
