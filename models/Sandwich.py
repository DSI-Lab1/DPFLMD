import numpy as np
import math
from models.seqUtils import *
import itertools
class FfpaServer():

    def __init__(self, args):
        self.args = args
        utils = seqUtils()
        self.candidate_pool = CandidatePool(self.args)
        self.accept_pool = AcceptPool(utils)

    def drawCandidate(self):
        return self.candidate_pool.mergeCpool

    def FirstGenCan(self,alphabet,minl):
        init_candidates = []
        can = itertools.product(alphabet, repeat=minl)
        for c in can:
            c = ''.join(c)
            init_candidates.append(c)
        for candi in init_candidates:
            self.initCandidate(candi)
        self.candidate_pool.mergeCpool = []
        alphabetS = ""
        for i in alphabet:
            alphabetS = alphabetS + i
        Mcan = itertools.product(alphabet, repeat=minl-1)
        for c in Mcan:
            cs = ""
            for j in c:
                cs = cs + j
            self.candidate_pool.mergeCpool.append(cs+alphabetS)

    def initCandidate(self, candidate):
        self.candidate_pool.newCandidate(candidate)

    def candidateNum(self):
        return len(self.candidate_pool.pool.keys())

    # Determine whether the server should stop asking
    def terminal(self,round,lmax,lmin):
        if round == lmax - lmin + 1:
            return True
        if self.candidateNum() == 0:
            return True
        return False

    def uploadSupportCount(self, update):
        for candidate, support in update.items():
            self.candidate_pool.updateResponse(candidate,support)

        accept = self.candidate_pool.leaveCheck()
        C,MergeC = self.accept_pool.addAccept(accept)

        self.candidate_pool.mergeCpool = MergeC
        new_candidates = set(C)
        for new_c in new_candidates:
            self.candidate_pool.newCandidate(new_c)
        return accept

class CandidatePool():

    def __init__(self, args):
        self.pool = {}
        self.mergeCpool = []
        self.args = args
        self.kprop = self.args.k
        self.leave_log = {}  # how many support got when leaving the pool
        self.alphabet = ["a","g","c","t"]
        self.thres = 100

    def newCandidate(self, candidate):
        self.pool[candidate] = [0, 0]

    def drawCandidate(self):
        return self.mergeCpool

    def updateResponse(self, candidate, res):
        # res:: 0: no; 1: yes
        self.pool[candidate][0] += res[0]
        self.pool[candidate][1] += res[1]

    def leaveCheck(self):
        accept = {}
        self.thres = self.kprop * (1 - self.args.eta) + (1 - self.kprop) * self.args.eta + math.sqrt(-math.log(self.args.xi) / (2 * self.args.num_participants))
        for k in self.pool.keys():
            if self.pool[k][1] / self.args.num_participants >= self.thres:
                accept[k]=self.pool[k][1]
                self.leave_log[k] = (self.pool[k][0] + self.pool[k][1], 'accept')

        self.pool = {}
        return accept

    def candidate_num(self):
        return len(self.pool.keys())

    def get_leave_log(self):
        return self.leave_log

class AcceptPool():
    def __init__(self, utils):
        self.pool = {}
        self.utils = utils
        self.candidate_history = set()
        # self.alphabet =  ["A", "G", "C", "T"]
        self.alphabet = ["a", "g", "c", "t"]

    def addAccept(self, accepts):
        for ac in accepts.keys():
            self.pool[ac]=accepts[ac]

        C = []
        MergeC = []
        S = ""
        for i in self.alphabet:
            S = S + i
        for ac in accepts.keys():
            MergeC.append(ac + S)
            for i in self.alphabet:
                C.append(ac + i)

        return C,MergeC

    def __normalizePool(self, pool):
        res = set()
        for subpool in pool.values():
            res.update(subpool)
        return res

    def output(self):
        return self.__normalizePool(self.pool)

    def outputSuper(self):
        return self.__normalizePool(self.super_pool)
