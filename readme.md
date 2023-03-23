# Causal Discovery Python Implement

Hello there! 👋 I'm a student studying Causal Discovery, and I've created this page to share my implemented codes. All the codes here have been implemented by using only *numpy, scipy, pandas*, and *matplotlib*.

While studying Causal Discovery, I found that there were few proper code implementation examples available online. Most of the code online used pre-existing package, such as networkx, dowhy, cdt, etc., which made it difficult to understand how the underlying algorithm **really** worked. (There is also a way to view the package code, but it is usually too complicated to read. 😓) As a result, I decided to implement the code myself based on research papers and books.

I've shared my code for the people who prefer to study while implementing the code themselves, rather than relying on pre-existing package. I recommend following the implementation procedure outlined below. I hope that my work will be helpful. 😁

<br>

## **I recommend it to people like this!**

- **Who wants to understand Causal Discovery algorithms while implementing them** 👦
- **Who wants to implement their own algorithm by modifying pre-existing algorithms** 👩

<br>

## Implementation Procedure


### 1️⃣ DAG Pattern

❗ **We don't use networkx. We will implement our own graph class. Visualization, too**

| Title | Implementation | Notebook url |
| --- | --- | --- |
| DAG Pattern_base | Foundation of DAG Pattern | [Click!](https://colab.research.google.com/drive/1cDxmQPL-v3egbrZVsklQDzbukHNVgeVq?usp=share_link) |
| DAG Pattern_d_separation | Methods related to d-separation | [Click!](https://colab.research.google.com/drive/1GZ6lX4RzSzSJriIe5_t-tRYZd4YULxoF?usp=share_link) |
| DAG Pattern_visualization | Visualization (Force-directed graph drawing) | [Click!](https://colab.research.google.com/drive/1hCDTh3zttekN6YFuvDiQpHd3YMrX7cIU?usp=share_link) |


### 2️⃣ Nonparametric CI Test

| Title | Implementation | Notebook url |
| --- | --- | --- |
| Nonparametric CI Test_MI | Conditional Mutual Information | [Click!](https://colab.research.google.com/drive/1n-62Din_vq5TY9zFrjxnXvK4iM2XQw9j?usp=share_link) |
| Nonparametric CI Test_KCIT | KCIT, Kernel-based Conditional Independence Test | [Click!](https://colab.research.google.com/drive/10Y37wFC4v3cl_7WNFheeUuH4iwKKREgq?usp=share_link) |


### 3️⃣ **Constraint-based Algorithm**

| Title | Implementation | Notebook url |
| --- | --- | --- |
| Constraint-based Algorithm_basic | Basic algorithm of Constraint-based Algorithm | [Click!](https://colab.research.google.com/drive/1Rrpdw1IlPNKN_yVqc1ZSFx_fzKfHdDtD?usp=share_link) |
| Constraint-based Algorithm_pc | PC algorithm | [Click!](https://colab.research.google.com/drive/1jhauXC8LsdViE8R58-9GuPRxdcNUUBC2?usp=share_link) |
| Constraint-based Algorithm_cpc | Conservative PC algorithm | [Click!](https://colab.research.google.com/drive/1NZMTB-jG8AaOBFiRdxGOohn2Q7j5tq31?usp=share_link) |
