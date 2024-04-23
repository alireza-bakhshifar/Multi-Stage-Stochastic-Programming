# Multi-Stage Stochastic Programming
The Python implementation of the Asset-Liability Management (ALM) compact and split variables model utilizes the Pyomo package. To tackle uncertainty, stochastic programming is used. This method can be split into two branches: chance-constrained programming and scenario generation. The scenario generation can be further divided into Two-Stage stochastic programming and Multi-Stage stochastic programming.

In the context of scenario generation, every realization of the uncertain parameter is considered a scenario. A scenario tree is typically created, and the best combination that fulfills the overall expected value or specific objective function is determined. To solve a multi-stage problem we can use many techniques. Compact model and split variables are two techniques to tackle multi-stage complex structure.
![image](https://github.com/alireza-bakhshifar/Multi-Stage-Stochastic-Programming/assets/59390030/65712385-8e67-4261-8c46-bab19d1b63e1)

