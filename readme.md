# Causal Discovery Python Implementation

Hi, there! 👋 I'm a student studying Causal Discovery, and this page is created to share my implemented codes. All the codes here are implemented by using only *numpy, scipy, pandas*, and *matplotlib*.

While studying Causal Discovery, I found that there were few proper code implementation examples online. Most of the code online used pre-existing package, such as networkx, dowhy, cdt, etc., which made it difficult to understand how the underlying algorithm **really** worked. (There is also a way to read the package code, but it is usually too complicated. 😓) As a result, I decided to implement the code myself based on research papers and books.

I share my code for the people who prefer to study while implementing the code themselves, rather than relying on pre-existing package. I recommend to follow **Implementation Procedure** below. I hope that my work will be helpful for you. 😁

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

<br>

## Reference
[1] Geiger, D., Verma, T., &#38; Pearl, J. (1990). d-Separation: From Theorems to Algorithms. In <i>Machine Intelligence and Pattern Recognition</i> (Vol. 10, Issue C)  
[2] Zhang, K., Peters, J., Janzing, D., &#38; Schölkopf, B. (2011). Kernel-based conditional independence test and application in causal discovery. <i>Proceedings of the 27th Conference on Uncertainty in Artificial Intelligence, UAI 2011</i>  
[3] Metropolitan. (2004). Learning Bayesian Networks. chapter 10.  
[4] Verma, T., Pearl, J. (1990). On the Equivalence of Causal Models. <i>Appears in Proceedings of the Sixth Conference on Uncertainty in Artificial Intelligence (UAI1990)</i>.  
[5] Meek, C. (1995). Causal inference and causal explanation with background knowledge. <i>Conference on Uncertainty in Artificial Intelligence.</i>  
[6] Ramsey, J., Spirtes, P., &#38; Zhang, J. (2006). Adjacency-faithfulness and conservative causal inference. <i>Proceedings of the 22nd Conference on Uncertainty in Artificial Intelligence, UAI 2006</i>.  
[7] Peter, J., Zanzing, D., Schölkopf, B. (2017). Elements of Causal Inference. <i>The MIT Press</i>  
