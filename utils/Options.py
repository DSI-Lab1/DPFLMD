import argparse

def args_parser():
    parser = argparse.ArgumentParser()
    # Motifs params
    parser.add_argument('--minl', type=int, default=5, help="Minimum length of motifs")
    parser.add_argument('--maxl', type=int, default=10, help="Maximum length of motifs")
    parser.add_argument('--topN', type=int, default=30, help="the value N in top-N")
    parser.add_argument('--delta', type=float, default=0.3, help="tolerance parameter")

    # Basic params
    parser.add_argument('--k', type=float, default=10000,
                        help="frequency threshold, when smaller than 1, it will be the proportion")
    parser.add_argument('--xi', type=float, default=0.1, help="allowed error rate for frequency estimation")
    parser.add_argument('--epsilon', type=float, default=10.0, help="param of LDP")
    parser.add_argument('--num_participants', type=int, default=100000, help="number of participating clients")
    parser.add_argument('--mode', type=str, default='FLMD', help="mode: FLMD || groundtruth")
    parser.add_argument('--num_candidate', type=int, default=1, help="candidates sent to each client")
    parser.add_argument('--duplicate', type=int, default=1, help="virtually duplicate the dataset")
    parser.add_argument('--process', type=int, default=0, help="number of worker processes, 0: single process")

    args = parser.parse_args()
    return args