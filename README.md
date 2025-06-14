# AI-Pagerank

PageRank Algorithm Implementation:


This project implements Google's PageRank algorithm using two different approaches: random sampling and iterative calculation. PageRank is the foundational algorithm that Google used to rank web pages in search results based on their importance and link structure.


Overview:


PageRank determines the importance of web pages by analyzing the link structure between pages. The core idea is that a page is important if other important pages link to it. This creates a recursive definition that can be solved using mathematical iteration or Monte Carlo sampling.

Algorithm Explanation:


Random Surfer Model:

The PageRank algorithm can be understood through the "random surfer" model:

- A hypothetical web surfer starts on a random page
- At each step, with probability d (damping factor ≈ 0.85), they follow a random link from the current page
- With probability 1-d, they jump to a completely random page in the corpus
- PageRank represents the long-term probability of finding the surfer on each page


Mathematical Formula:

For each page p, PageRank is calculated as:
PR(p) = (1-d)/N + d × Σ(PR(i)/NumLinks(I))


Where:

- d = damping factor (0.85)
- N = total number of pages
- i = pages that link to page p
- NumLinks(i) = number of outgoing links from page i
