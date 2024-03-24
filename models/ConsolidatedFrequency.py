from collections import Counter
import Levenshtein

def TopN(dicta,dictb, top_K):
    dictMerged = dict(list(dicta.items()) + list(dictb.items()))
    d = sorted(dictMerged.items(),key=lambda t:t[1],reverse=True)[:top_K]
    return dict(d)

def calculateConsolidatedFrequency(args,FPs):
    len_gram_sup = {}
    # Step 1: put all l-motifs into different sets.
    for p in FPs:
        curLen = len(p)
        if curLen >= args.minl and curLen <= args.maxl:
            if curLen in len_gram_sup.keys():
                counter = len_gram_sup[curLen]
                counter[p] = FPs[p]
                len_gram_sup[curLen] = counter
            else:
                counter = Counter()
                counter[p] = FPs[p]
                len_gram_sup[curLen] = counter

    N = {}
    l = args.minl
    len_motifs_consolidatesup = {}

    while l <= args.maxl:
        if l in len_gram_sup:
            seq_l = len_gram_sup[l]
            s = list(seq_l.keys())[0]
            Bucket = {}
            for each_seq1 in seq_l:
                i = Levenshtein.hamming(each_seq1, s)
                if i not in Bucket.keys():
                    Bucket.setdefault(i, [])
                    Bucket[i].append(each_seq1)
                else:
                    Bucket[i].append(each_seq1)
            for i in Bucket.keys():
                for each_seq1 in Bucket[i]:
                    len_motifs_consolidatesup.setdefault(l, {})[each_seq1] = 0
                    if i >= args.delta:
                        for j in range(int(i - args.delta), min(int(i + args.delta), l) + 1):
                            if j in Bucket.keys():
                                for each_seq2 in Bucket[j]:
                                    if 0 <= Levenshtein.hamming(each_seq1, each_seq2) <= args.delta:
                                        len_motifs_consolidatesup.setdefault(l, {})[each_seq1] = round(
                                            float(len_motifs_consolidatesup.setdefault(l, {})[each_seq1])) + round(
                                            float(len_gram_sup[l][each_seq2]))

                    else:
                        for j in range(0, min(int(i + args.delta), 1) + 1):
                            if j in Bucket.keys():
                                for each_seq2 in Bucket[j]:
                                    if 0 <= Levenshtein.hamming(each_seq1, each_seq2) <= args.delta:
                                        len_motifs_consolidatesup.setdefault(l, {})[each_seq1] = round(
                                            float(len_motifs_consolidatesup.setdefault(l, {})[each_seq1])) + round(
                                            float(len_gram_sup[l][each_seq2]))

            N = TopN(N, len_motifs_consolidatesup[l],args.topN)
        l += 1
    return N