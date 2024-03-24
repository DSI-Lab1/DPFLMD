import datetime
import math

from models.GroundTruth import groundTruth
from utils.Options import args_parser
from models.Handlers import flmdHandler
import models.ConsolidatedFrequency as CF

def GetF1score(result,truth):
    tp = 0
    for frag in result:
        if frag in truth:
            tp += 1
    fp = len(result) - tp
    precision = tp/len(result)
    recall = tp/len(truth)
    F1score = (2*precision*recall)/(precision+recall)
    return F1score

def GetARE(result,truth):
    ARE = 0.0
    for key in truth:
        if key in result:
            ratio = abs(result[key] - truth[key])/ truth[key]
            ARE += ratio
        else:
            ARE += 0
    ARE = ARE / len(truth)
    return ARE


def GetPrecision(result,truth):
    tp = 0
    for frag in result:
        if frag in truth:
            tp += 1
    precision = tp/len(result)
    return precision

if __name__ == '__main__':

    args = args_parser()

    file = open("Dataset/DP-MFSC_Dataset/Promoters.txt")
    lines = file.readlines()
    dataset = []
    for line in lines:
        dataset.append(line.strip())

    # Implement the DP-FLMD Model
    if args.mode == 'FLMD':
        # Phase 1: Mining frequent sequence sets
        begin = datetime.datetime.now()
        handler = flmdHandler(args, dataset)
        fragments = handler.run()
        end = datetime.datetime.now()
        print("DP-FLMD minning FPs running time:" + str(end - begin))

        # Phase 2: Mining top-k Consolidated frequency sequences
        CF_Noise = CF.calculateConsolidatedFrequency(args, fragments)
        end = datetime.datetime.now()
        print("DP-FLMD All running time:" + str(end - begin))

        # Implement the groundtruth Model
        # Phase 1: Mining frequent sequence sets
        res = groundTruth(dataset, args)
        # Phase 2: Mining top-k Consolidated frequency sequences
        CF_True = CF.calculateConsolidatedFrequency(args, res)

        # Evaluate results
        ARE = GetARE(CF_Noise, CF_True)
        F1Score = GetF1score(CF_Noise, CF_True)
        precision = GetPrecision(CF_Noise.keys(), CF_True.keys())
        print("time:", str(end - begin),", precision: ", precision, ", ARE: ", ARE, ",  F1Score: ",F1Score)

    # Implement the groundtruth model
    else:
        begin = datetime.datetime.now()
        # Phase 1: Mining frequent sequence sets
        res = groundTruth(dataset, args)
        print("res: ", res)
        # Phase 2: Mining top-k Consolidated frequency sequences
        CF_True = CF.calculateConsolidatedFrequency(args, res)
        print("CF_True: ", CF_True)
        end = datetime.datetime.now()
        print("GroundTruth Total running time:" + str(end - begin))
