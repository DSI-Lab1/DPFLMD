# DP-FLMD
This repo hosts the code for paper "Privacy-Preserving Federated Discovery of DNA Motifs with Differential Privacy", Expert Systems With Applications, Chen, Yao and Gan, Wensheng and Huang, Gengsen and Wu, Yongdong and Philip, S Yu, 2024.

## Requirements
Python programming language.

## Running the program
python main.py --mode=FLMD --num_candidate=1 --num_participants=261 --k=0.01 --epsilon=3 --minl=1 --maxl=4 --topN=30 --delta=1 --xi=0.01 --process=14

## Introduction
DP-FLMD is a privacy-preserving federated framework for discovering DNA sequence motifs. We employ federated learning and differential privacy, allowing participants to store their raw data locally and upload only selected parameters to protect data privacy. DP-FLMD uses a query-response method between the server and participants. The server sends sequences to participants for querying. The participants send simple binary answers to respond to the queries from the server, where the binary answers are obtained by the participants executing the LDP method. Then, the server discovers motifs according to the response results of multiple rounds.

## Dataset
We used six DNA datasets, including promoters(https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/promoter-gene-sequences/promoters.data), washington(http://bio.cs.washington.edu/assessment/download.html), chrUn(https://hgdownload.soe.ucsc.edu/goldenPath/mm39/chromosomes/chrUn_MU069435v1.fa.gz), splice(https://archive.ics.uci.edu/ml/machine-learning-databases/molecular-biology/splice-junction-gene-sequences), chrY(https://hgdownload.soe.ucsc.edu/goldenPath/mm39/chromosomes/chrY_JH584301v1_random.fa.gz), and centers(https://github.com/microsoft/clustered-nanopore-reads-dataset). 

## Citation 
If this article or code useful for your project, please refer to
```
@article{chen2024privacy,
  title={Privacy-Preserving Federated Discovery of DNA Motifs with Differential Privacy},
  author={Chen, Yao and Gan, Wensheng and Huang, Gengsen and Wu, Yongdong and Philip, S Yu},
  journal={Expert Systems With Applications},
  year={2024}
}
```

## Notes
If there are any questions, please contact us (Email: csyaochen@gmail.com).