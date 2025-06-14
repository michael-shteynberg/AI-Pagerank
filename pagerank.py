import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    
    N = len(corpus)
    result = {}
    base_prob = (1 - damping_factor) / N
    
    # Give every page the base probability
    for p in corpus:
        result[p] = base_prob
    
    # Get links from current page
    links = corpus[page]
    
    # Special case: if no links, pretend it links to everything
    if len(links) == 0:
        links = set(corpus.keys())
    
    # Add extra probability for linked pages
    if len(links) > 0:
        extra_prob = damping_factor / len(links)
        for linked_page in links:
            result[linked_page] += extra_prob
    
    return result


def sample_pagerank(corpus, damping_factor, n):
    
    page_counts = {}
    for page in corpus:
        page_counts[page] = 0

    current_page = random.choice(list(corpus.keys()))
    page_counts[current_page] += 1

    for i in range(n - 1):
        probabilities = transition_model(corpus, current_page, damping_factor)
        pages = list(probabilities.keys())
        weights = list(probabilities.values())
        next_page = random.choices(pages, weights, k=1)[0]
        page_counts[next_page] += 1
        current_page = next_page

    result = {}
    for page in page_counts:
        result[page] = page_counts[page] / n
    return result


def iterate_pagerank(corpus, damping_factor):
    
    N = len(corpus)
    
    pagerank = {}
    for page in corpus:
        pagerank[page] = 1 / N
    
    incoming_links = {}
    for page in corpus:
        incoming_links[page] = []
    
    for page in corpus:
        if len(corpus[page]) == 0:
            for all_pages in corpus:
                incoming_links[all_pages].append(page)
        else:
            for linked_page in corpus[page]:
                incoming_links[linked_page].append(page)

    while True:
        new_pagerank = {}
    
        for p in corpus:
            base_prob = (1 - damping_factor) / N

            link_sum = 0
            for i in incoming_links[p]:
                num_links = len(corpus[i]) if len(corpus[i]) > 0 else N
                link_sum += pagerank[i] / num_links
            
            new_pagerank[p] = base_prob + damping_factor * link_sum

        converged = True
        for page in corpus:
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:
                converged = False
                break

        if converged:
            break
        else:
            pagerank = new_pagerank
            
    return pagerank


if __name__ == "__main__":
    main()