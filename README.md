# mac6916

#### Python environment

Creating an environment from the `environment.yml` file:
```
conda env create -f environment.yml
```

#### Bayes Ball

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
