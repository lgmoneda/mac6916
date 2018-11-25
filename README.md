# mac6916

## Index

1. [Python Environment](python-environment)
2. [Bayes Ball (L3Q4)](bayes-ball)
3. [Markov Partition (L4Q3)](markov-partition)

## Python environment

Creating an environment from the `environment.yml` file:
```
conda env create -f environment.yml
```

## Bayes Ball

Just run `python bayes-ball/bayes_ball.py`.

To add new examples using the Asia network you'll need to edit the script. The network is already on it as:

```
A = node("Visit to (A)sia")
T = node("(T)uberculosis")
E = node("(E)ither")
X = node("(X)-ray")
D = node("(D)yspnoea")
L = node("(L)ung cancer")
S = node("(S)moking")
B = node("(B)ronchitis")
```

Use the letters to check d-separation as follows:
``` 1c-enterprise
check_dseparation(A, L, [E], network)
```

It checks if A and L are d-separated given E.

## Markov Partition

Run:

``` 1c-enterprise
python markov/markov.py misconception.uai
```

The `misconception.uai` file comes from an example from this [book](### http://www.cs.cmu.edu/~epxing/Class/10708-13/reading/Ch%204.pdf). The partition result match the one in the book (page 105, figure 4.2 legend).

The example given pic 2011] is on the `problem.uai` file.

An example of bayesian network encoded by the undirected graph can be found on the `bayesian.uai` file:

Structure: B <- A -> C

| A        | P(A)           |
| ------------- |:-------------:|
| 0      | 0.4 |
| 1      | 0.6      |


| A             | B               | P(B \| A) | P(A, B)|
| ------------- | :-------------: |:---:|:---:|
| 0             | 0             | 0.4 | 0.16   |
| 0             | 1             | 0.3 | 0.12   |
| 1             | 0             | 0.3 | 0.36   |
| 1             | 1             | 0.3 | 0.42   |

| A             | C               | P(C \| A) | P(A, C)|
| ------------- | :-------------: |:---:|:---:|
| 0             | 0             | 0.1 | 0.04   |
| 0             | 1             | 0.2 | 0.08   |
| 1             | 0             | 0.9 | 0.24   |
| 1             | 1             | 0.8 | 0.48   |
