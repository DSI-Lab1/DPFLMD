import itertools


class SeqDataSet():
    def __init__(self, points):
        # self.alphabet =  ["A", "G", "C", "T"]
        self.alphabet = ["a", "g", "c", "t"]
        self.points =  self.alphabet
        self.record = []

    def add_line(self, line):
        self.record.append(line)

    def get_line(self, index):
        return self.record[index]

    def get_line_num(self):
        return len(self.record)

    def __getitem__(self, index):
        return self.get_line(index)

    def init_candidate(self,k):
        candidates = []
        can = itertools.product(self.alphabet, repeat=k)
        for c in can:
            c = ''.join(c)
            candidates.append(c)
        return candidates